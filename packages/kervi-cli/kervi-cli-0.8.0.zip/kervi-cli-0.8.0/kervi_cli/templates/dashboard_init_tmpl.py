""" bootstrap your kervi dashboards here """
from kervi.dashboard import Dashboard, Camboard, DashboardSection

#Create the dashboards for your Kervi application here.

#A camboard is a special dashbord where the background is a video feed.
#is_default signals that this dashbord is shown first in the ui,
#cam1 is the id of the camera that should be used as video source.
MAIN = Camboard("cam", "Main", "cam1", is_default=True)
MAIN.add_section(DashboardSection("section1"))

#Standard dashboard with several sections where sensors are placed.
#Each sensor linkes to one or more dashboard sections 
SYSTEM = Dashboard("system", "System")
SYSTEM.add_section(DashboardSection("cpu", ui_columns=2, ui_collapsed=True))
SYSTEM.add_section(DashboardSection("memory", ui_columns=2, ui_collapsed=True))
SYSTEM.add_section(DashboardSection("log", ui_columns=2, ui_title="Log", user_log=True))
SYSTEM.add_section(DashboardSection("disk", ui_columns=2))
SYSTEM.add_section(DashboardSection("power", ui_columns=1, ui_rows=2, ui_title="Power"))
