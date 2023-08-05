from eureqa.analysis.components.base import _Component
from eureqa.utils.jsonrest import _JsonREST
from eureqa.analysis.analysis_file import AnalysisFile

class TabbedLayout(_Component):
    """
    TabbedLayout component

    Lets users pick to see other components based on titles (works with a few items). Similar to :py:class:`~eureqa.analysis.components.dropdown_layout.DropdownLayout` but suited to smaller lists

    For example::

        t = TabbedLayout()
        t.add_component(title="choice 1", component=HtmlBlock("This is item 1"))
        t.add_component(title="choice 2", component=HtmlBlock("This is item 2"))
        analysis.create_card(t)

    """

    _component_type_str = 'TABBED_LAYOUT'

    def __init__(self, _tabs=None, _analysis=None, _component_id=None, _component_type=None):
        # Tabs to add as soon as we are _associate()'d
        # Note that `_queued_tabs` are _Tab objects and `_tabs` are JSON dictionaries
        self._queued_tabs = []

        if _tabs is not None:
            self._queued_tabs = _tabs

        super(TabbedLayout, self).__init__(_analysis=_analysis, _component_id=_component_id,
                                           _component_type=_component_type)

    class _Tab(object):
        def __init__(self, title, component, icon=None):
            """
            :param str label: Tab label
            :param ~eureqa.analysis.components.base._Component component: Tab contents, as a Component
            :param ~eureqa.analysis.analysis_file.AnalysisFile label_img: Tab label image (optional) -- must be a file containing an image
            """
            self._title = title
            self._component = component
            self._icon = icon

        def _associate(self, analysis):
            if self._icon is not None and not isinstance(self._icon, AnalysisFile):
                self._icon = AnalysisFile.create(analysis, self._icon)
            self._component._associate(analysis)

        def __repr__(self):
            return repr([self._title, self._component, self._icon[:32] if self._icon else self._icon])

        def _to_json(self):
            return {
                "label": self._title,
                "component_id": self._component._component_id,
                "icon_file_id": self._icon._file_id if getattr(self, "_icon", None) is not None else None
            }

    def add_component(self, title, component, icon=None):
        """
        Add a new tab containing a new component

        :param str title: Title of the tab
        :param eureqa.analysis.components.base._Component component: Content of the tab
        :param str icon: (Optional) Icon for the tab, as either a str() containing the file-data for an image, or an :class:`AnalysisFile` containing an image
        """
        new_tab = TabbedLayout._Tab(title, component, icon)

        if hasattr(self, "_analysis"):
            new_tab._associate(self._analysis)
            if not hasattr(self, "_tabs"):
                self._tabs = []
            self._tabs.append(new_tab._to_json())
        else:
            self._queued_tabs.append(new_tab)

    def _associate(self, analysis):
        if not hasattr(self, "_tabs"):
            self._tabs = []

        for new_tab in self._queued_tabs:
            new_tab._associate(analysis)
            self._tabs.append(new_tab._to_json())
        self._queued_tabs = []

        super(TabbedLayout, self)._associate(analysis)

    def _fields(self):
        return super(TabbedLayout, self)._fields() + [ 'tabs' ]
