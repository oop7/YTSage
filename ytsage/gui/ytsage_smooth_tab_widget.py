from PySide6.QtCore import QEasingCurve, QPropertyAnimation, Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QFrame,
    QGraphicsOpacityEffect,
    QLabel,
    QScrollArea,
    QStackedWidget,
    QTabBar,
    QVBoxLayout,
    QWidget,
)


class WheelScrollableTabBar(QTabBar):
    """Scroll the tab strip horizontally with the mouse wheel."""

    def __init__(self, scroll_area: QScrollArea, parent=None):
        super().__init__(parent)
        self._scroll_area = scroll_area

    def wheelEvent(self, event) -> None:
        delta = event.pixelDelta().x() or event.pixelDelta().y()
        if not delta:
            delta = event.angleDelta().x() or event.angleDelta().y()

        if not delta:
            event.ignore()
            return

        scroll_bar = self._scroll_area.horizontalScrollBar()
        scroll_bar.setValue(scroll_bar.value() - delta)
        event.accept()


class FadingStackedWidget(QStackedWidget):
    """
    A QStackedWidget that cross-fades between widgets.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.fade_duration = 300 
        self.fade_easing = QEasingCurve.Type.OutQuad

    def setCurrentIndex(self, index):
        curr_index = self.currentIndex()
        if index == curr_index:
            return

        widget = self.widget(index)
        curr_widget = self.widget(curr_index)
        
        # If widget isn't visible or valid, just swap
        if not self.isVisible() or not curr_widget:
            super().setCurrentIndex(index)
            return

        # 1. Capture the current view (the "old" tab)
        # Use grab() for simplicity and reliability in PySide6
        pixmap = self.grab()
        
        # 2. Create an overlay label to hold this "old" view
        overlay = QLabel(self)
        overlay.setPixmap(pixmap)
        overlay.setGeometry(0, 0, self.width(), self.height())
        overlay.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents) # Don't block clicks
        overlay.show()
        
        # 3. Switch the actual stack to the "new" view
        super().setCurrentIndex(index)
        
        # CRITICAL: Ensure overlay stays on top of the new widget
        overlay.raise_()
        
        # 4. Fade OUT the overlay, revealing the new view
        effect = QGraphicsOpacityEffect(overlay)
        overlay.setGraphicsEffect(effect)

        
        anim = QPropertyAnimation(effect, b"opacity", overlay)
        anim.setDuration(self.fade_duration)
        anim.setStartValue(1.0)
        anim.setEndValue(0.0)
        anim.setEasingCurve(self.fade_easing)
        
        # Cleanup when done
        anim.finished.connect(lambda: self._cleanup(overlay))
        
        # Keep reference to prevent GC
        self._active_anim = anim 
        anim.start(QPropertyAnimation.DeletionPolicy.DeleteWhenStopped)

    def _cleanup(self, overlay):
        overlay.hide()
        overlay.deleteLater()


class SmoothTabWidget(QWidget):
    """
    A unified Widget that behaves like a QTabWidget but uses smooth fading transitions.
    Includes a QTabBar and a FadingStackedWidget.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Main Layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        
        # Tab Bar
        self.tab_bar_scroll_area = QScrollArea(self)
        self.tab_bar_scroll_area.setWidgetResizable(False)
        self.tab_bar_scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.tab_bar_scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.tab_bar_scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        self.tab_bar_scroll_area.setAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        )
        self.tab_bar = WheelScrollableTabBar(self.tab_bar_scroll_area)
        self.tab_bar.setDrawBase(False) # We draw border on content instead
        self.tab_bar.setElideMode(Qt.TextElideMode.ElideNone)
        self.tab_bar.setExpanding(False)
        self.tab_bar.setUsesScrollButtons(False)
        self.tab_bar_scroll_area.setWidget(self.tab_bar)
        self.layout.addWidget(self.tab_bar_scroll_area)
        self.tab_bar.currentChanged.connect(self.set_current_index)
        
        # Content Area (Frame) - Mimics QTabWidget::pane
        self.content_frame = QFrame(self)
        self.content_frame.setObjectName("tabContent") 
        
        # Layout inside the content frame
        self.content_layout = QVBoxLayout(self.content_frame)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(0)
        
        # The Stack
        self.stack = FadingStackedWidget(self.content_frame)
        self.content_layout.addWidget(self.stack)
        
        self.layout.addWidget(self.content_frame)

    def addTab(self, widget, label):
        """Add a tab with the given widget and label."""
        self.stack.addWidget(widget)
        self.tab_bar.addTab(label)
        self.refresh_tab_bar_size()

    def refresh_tab_bar_size(self) -> None:
        """Resize the tab strip after tab text or styling changes."""
        self.tab_bar.ensurePolished()
        tab_bar_size = self.tab_bar.sizeHint()
        tabs_width = sum(
            self.tab_bar.tabRect(index).width()
            for index in range(self.tab_bar.count())
        )
        tab_width = max(
            tab_bar_size.width(),
            tabs_width,
        )
        self.tab_bar.setFixedSize(tab_width, tab_bar_size.height())
        self.tab_bar_scroll_area.setFixedHeight(tab_bar_size.height())

    def set_current_index(self, index):
        """Slot to handle tab bar clicks."""
        self.tab_bar.setCurrentIndex(index)
        self.stack.setCurrentIndex(index)

    def currentWidget(self):
        return self.stack.currentWidget()

    def currentIndex(self):
        return self.stack.currentIndex()
