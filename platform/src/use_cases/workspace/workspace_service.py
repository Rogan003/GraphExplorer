from django.core.files.storage import FileSystemStorage
from use_cases.workspace.workspace import Workspace
from graph_explorer_api.model.graph import Graph

def _get_workspaces(session):
    return session.get("workspaces", [])

def _add_workspace(session, workspace):
    workspaces = _get_workspaces(session)
    workspaces.append(workspace.to_dict())
    session["workspaces"] = workspaces
    session.modified = True


def update_workspace_in_session(session, ws):
    workspaces = _get_workspaces(session)
    if 0 <= ws.id < len(workspaces):
        workspaces[ws.id] = ws.to_dict()
        session["workspaces"] = workspaces
        session.modified = True

def handle_initial_workspace(session, plugin_service, tree_view_service):
    workspaces = _get_workspaces(session)
    if not workspaces:
        ws = Workspace(id=0)
        ws.load_graph(plugin_service, tree_view_service)
        ws.show_graph(plugin_service, tree_view_service)
        _add_workspace(session, ws)
        workspaces = _get_workspaces(session)
    return workspaces

def upload_file(request):
    if request.method == "POST" and request.FILES.get("file"):
        fs = FileSystemStorage()
        filename = fs.save(request.FILES["file"].name, request.FILES["file"])
        return fs.path(filename)
    return None

def get_active_workspace(session, ws_id, visualizer=None, datasource=None, plugin_service=None, tree_view_service=None, path=None, data_source_config=None):
    workspaces = _get_workspaces(session)
    if not workspaces or not (0 <= ws_id < len(workspaces)):
        return None, workspaces

    ws_dict = workspaces[ws_id].copy()
    ws_dict.pop("graph", None)
    
    ws = Workspace(**ws_dict)

    if "graph_data" in ws_dict and ws_dict["graph_data"] is not None:
        ws.graph = Graph.from_dict(ws_dict["graph_data"])

    ws.tree_view = tree_view_service.empty_tree()
    if path:
        ws.path = path
    if datasource:
        ws.data_source_identifier = datasource
    if visualizer:
        ws.visualizer_identifier = visualizer
    if data_source_config:
        ws.configuration.update(**data_source_config)
    if plugin_service and tree_view_service:
        if ws.graph is None or not ws.graph.nodes:
            ws.load_graph(plugin_service, tree_view_service)
        ws.graph_html = ws.show_graph(plugin_service, tree_view_service)

    update_workspace_in_session(session, ws)
    workspaces = _get_workspaces(session)
    return ws, workspaces

def create_workspace(session, path=None, datasource=None, visualizer=None, plugin_service=None, tree_view_service=None,
                     data_source_config=None):
    workspaces = _get_workspaces(session)
    ws = Workspace(
        id=len(workspaces),
        path=path,
        data_source_identifier=datasource,
        visualizer_identifier=visualizer,
        data_source_configuration=data_source_config
    )

    if plugin_service and tree_view_service:
        if ws.graph is None:
            ws.load_graph(plugin_service, tree_view_service)
        ws.graph_html = ws.show_graph(plugin_service, tree_view_service)

    _add_workspace(session, ws)
    workspaces = _get_workspaces(session)
    return ws, workspaces

def save_workspace(session, ws):
    ws.graph_data = ws.graph.to_dict()
    update_workspace_in_session(session, ws)

def get_config_for_workspace(session, ws_id: int) -> dict:
    workspaces = _get_workspaces(session)

    for workspace in workspaces:
        if workspace["id"] == ws_id:
            return workspace["data_source_configuration"]
