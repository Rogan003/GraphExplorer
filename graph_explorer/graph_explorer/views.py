from django.shortcuts import render
from django.apps import apps
from django.http import JsonResponse
from use_cases.const import DATA_SOURCE_GROUP, VISUALIZER_GROUP
from use_cases.workspace.workspace_service import (
    handle_initial_workspace,
    upload_file,
    get_active_workspace,
    create_workspace,
)
from use_cases.cli.command_executor import execute_command
from use_cases.cli.command_parser import parse_command

def index(request):
    # request.session.flush()
    plugin_service = apps.get_app_config("graph_explorer").plugin_service
    tree_view_service = apps.get_app_config("graph_explorer").tree_view_service

    workspaces = handle_initial_workspace(request.session, plugin_service, tree_view_service)

    file_path = upload_file(request)

    active_ws_id = int(request.GET.get("tab", len(workspaces)))
    new_ws_flag = request.GET.get("new_workspace") == "true"

    if new_ws_flag:
        active_workspace, workspaces = create_workspace(
            request.session,
            file_path=file_path,
            datasource=request.GET.get("datasource"),
            visualizer=request.GET.get("visualizer"),
            plugin_service=plugin_service,
            tree_view_service=tree_view_service,
        )
    else:
        active_workspace, workspaces = get_active_workspace(
            request.session,
            active_ws_id,
            file_path=file_path,
            datasource=request.GET.get("datasource"),
            visualizer=request.GET.get("visualizer"),
            plugin_service=plugin_service,
            tree_view_service=tree_view_service,
        )

    return render(request, "index.html", {
        "visualizer_plugins": plugin_service.plugins[VISUALIZER_GROUP],
        "data_source_plugins": plugin_service.plugins[DATA_SOURCE_GROUP],
        "graph_html": active_workspace.graph_html if active_workspace else "No graph yet",
        "selected_visualizer_identifier": active_workspace.visualizer_identifier if active_workspace else None,
        "selected_data_source_identifier": active_workspace.data_source_identifier if active_workspace else None,
        "tree_view": active_workspace.tree_view if active_workspace else None,
        "workspaces": workspaces,
        "active_workspace_id": active_ws_id,
    })


def cli_execute(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST supported"}, status=405)

    cmd_str = request.POST.get("command")
    if not cmd_str:
        return JsonResponse({"error": "No command provided"}, status=400)

    command = parse_command(cmd_str)

    plugin_service = apps.get_app_config("graph_explorer").plugin_service
    tree_view_service = apps.get_app_config("graph_explorer").tree_view_service

    active_ws_id = int(request.GET.get("tab", 0))
    active_ws, workspaces = get_active_workspace(
        request.session,
        active_ws_id,
        plugin_service=plugin_service,
        tree_view_service=tree_view_service,
    )

    if not active_ws:
        return JsonResponse({"error": "No active workspace"}, status=400)

    result = execute_command(command, active_ws)
    active_ws.refresh_visualization(plugin_service)
    request.session["workspaces"] = [
        ws.to_dict() if hasattr(ws, "to_dict") else ws
        for ws in workspaces
    ]
    request.session.modified = True
    
    print("ACTIVE_WS ID: " + str(active_ws_id))
    print("ACTIVE_WS GRAPH_HTML: " + str(active_ws.graph_html))

    return JsonResponse({
        "result": result,
        "graph_html": active_ws.graph_html,
    })
