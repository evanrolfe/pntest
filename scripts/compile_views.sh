# Clients Page:
pyside2-uic src/views/clients/clients_page.ui > src/views/_compiled/clients/ui_clients_page.py
pyside2-uic src/views/clients/clients_table.ui > src/views/_compiled/clients/ui_clients_table.py
pyside2-uic src/views/clients/client_view.ui > src/views/_compiled/clients/ui_client_view.py

# Crawls Page:
pyside2-uic src/views/crawls/crawls_page.ui > src/views/_compiled/crawls/ui_crawls_page.py
pyside2-uic src/views/crawls/crawls_table.ui > src/views/_compiled/crawls/ui_crawls_table.py
pyside2-uic src/views/crawls/crawl_view.ui > src/views/_compiled/crawls/ui_crawl_view.py
pyside2-uic src/views/crawls/new_crawl.ui > src/views/_compiled/crawls/ui_new_crawl.py

# Network Page:
pyside2-uic src/views/network/network_page_widget.ui > src/views/_compiled/network/ui_network_page_widget.py
pyside2-uic src/views/network/network_requests_table_tabs.ui > src/views/_compiled/network/ui_network_requests_table_tabs.py
pyside2-uic src/views/network/network_requests_table.ui > src/views/_compiled/network/ui_network_requests_table.py
pyside2-uic src/views/network/network_display_filters.ui > src/views/_compiled/network/ui_network_display_filters.py
pyside2-uic src/views/network/network_capture_filters.ui > src/views/_compiled/network/ui_network_capture_filters.py

# Intercept Page:
pyside2-uic src/views/intercept/intercept_page.ui > src/views/_compiled/intercept/ui_intercept_page.py

# Editor Page:
pyside2-uic src/views/editor/request_edit_page.ui > src/views/_compiled/editor/ui_request_edit_page.py
pyside2-uic src/views/editor/editor_page.ui > src/views/_compiled/editor/ui_editor_page.py
pyside2-uic src/views/editor/request_body_form.ui > src/views/_compiled/editor/ui_request_body_form.py
pyside2-uic src/views/editor/request_headers_form.ui > src/views/_compiled/editor/ui_request_headers_form.py

# Shared:
pyside2-uic src/views/shared/request_view.ui > src/views/_compiled/shared/ui_request_view.py
pyside2-uic src/views/shared/loader.ui > src/views/_compiled/shared/ui_loader.py

# HACK: pyside2-uic does not import the QWebEngineView so we have to add this line manually:
# BE CAREFUL when changing this file as this line will easily break!
line=`sed "15q;d" src/views/_compiled/shared/ui_request_view.py`
if ! [[ $line =~ "qwebengineview" ]]; then
  echo "WARNING: src/views/_compiled/shared/ui_request_view.py does not contain qwebengineview on line 15 as expected.";
fi

sed -i '15s/.*/from PySide2.QtWebEngineWidgets import QWebEngineView/' src/views/_compiled/shared/ui_request_view.py
# /HACK

# Mainwindow:
pyside2-uic src/views/new_client_modal.ui > src/views/_compiled/ui_new_client_modal.py
pyside2-uic src/views/main_window.ui > src/views/_compiled/ui_main_window.py
