import bpy
import socket
import json
import threading
import time

# Globals for the socket and data
HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server
server_socket = None
client_socket = None
is_server_running = False
live_data = None
landmark_objects = []

def create_landmark_objects():
    """Creates 68 empty objects in the Blender scene to represent landmarks."""
    global landmark_objects
    if not landmark_objects:
        for i in range(68):
            obj_name = f"Landmark_{i:02d}"
            # Check if the object already exists
            if obj_name not in bpy.data.objects:
                bpy.ops.object.empty_add(type='PLAIN_AXES', radius=0.05, location=(0, 0, 0))
                new_obj = bpy.context.active_object
                new_obj.name = obj_name
                landmark_objects.append(new_obj)
            else:
                landmark_objects.append(bpy.data.objects[obj_name])
    
    print("68 empty objects created/found.")

def update_landmarks_from_data():
    """Updates the position of the landmark objects based on received data."""
    if live_data and landmark_objects:
        # The received data is a list of [x, y] coordinates from the video frame.
        # We'll use them to position the Blender objects. Note that the Z-axis
        # is set to 0 as this is a 2D-to-3D projection.
        for i, (x, y) in enumerate(live_data):
            if i < len(landmark_objects):
                landmark_objects[i].location.x = x * 0.01  # Scale coordinates for Blender
                landmark_objects[i].location.y = -y * 0.01 # Invert Y and scale
                landmark_objects[i].location.z = 0.0


def handle_client_connection():
    """A thread function to handle receiving data from the client."""
    global client_socket, live_data, is_server_running
    print("Waiting for client connection...")
    
    try:
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")
    except socket.timeout:
        # Timeout occurred, server is likely stopping
        if is_server_running:
            threading.Timer(1, handle_client_connection).start()
        return
    except Exception as e:
        print(f"Error accepting client connection: {e}")
        return

    while is_server_running:
        try:
            # First, read the size of the incoming message
            data_size_str = client_socket.recv(10).decode('utf-8')
            if not data_size_str:
                break
            
            data_size = int(data_size_str.strip())
            
            # Now, read the actual data
            data = b''
            while len(data) < data_size:
                packet = client_socket.recv(data_size - len(data))
                if not packet:
                    break
                data += packet
            
            if data:
                live_data = json.loads(data.decode('utf-8'))
        
        except (socket.error, ConnectionResetError):
            print("Client disconnected.")
            break
        except json.JSONDecodeError:
            print("Invalid JSON data received.")
            break
    
    if client_socket:
        client_socket.close()

def start_server():
    """Starts the socket server in a new thread."""
    global server_socket, is_server_running
    if is_server_running:
        print("Server is already running.")
        return

    is_server_running = True
    create_landmark_objects()

    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        server_socket.settimeout(1) # Add a timeout to allow for thread shutdown
        
        # Start the thread to handle the client connection
        client_thread = threading.Thread(target=handle_client_connection)
        client_thread.daemon = True # Thread exits when main program exits
        client_thread.start()

        print("Server started. Listening for connections...")
        
    except socket.error as e:
        print(f"Failed to start server: {e}. Is another program using port {PORT}?")
        is_server_running = False

def stop_server():
    """Stops the socket server."""
    global server_socket, is_server_running
    if not is_server_running:
        print("Server is not running.")
        return

    is_server_running = False
    if server_socket:
        print("Shutting down server...")
        server_socket.close()
        server_socket = None

# A simple timer to update the scene
def update_timer():
    if is_server_running:
        update_landmarks_from_data()
        return 0.016 # Update approximately every 60 frames per second
    return None

# Blender Panel
class MOCAP_PT_Panel(bpy.types.Panel):
    bl_label = "Live Landmark Capture"
    bl_idname = "MOCAP_PT_PANEL"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Landmarks'

    def draw(self, context):
        layout = self.layout
        
        if not is_server_running:
            layout.operator("mocap.start_server", text="Start Server")
        else:
            layout.operator("mocap.stop_server", text="Stop Server")
            layout.label(text="Server running. Connect from Python script.")

# Blender Operator to start the server
class MOCAP_OT_StartServer(bpy.types.Operator):
    bl_idname = "mocap.start_server"
    bl_label = "Start Server"
    bl_description = "Starts the socket server to receive landmark data."

    def execute(self, context):
        start_server()
        # Register the timer to update the scene
        bpy.app.timers.register(update_timer)
        return {'FINISHED'}

# Blender Operator to stop the server
class MOCAP_OT_StopServer(bpy.types.Operator):
    bl_idname = "mocap.stop_server"
    bl_label = "Stop Server"
    bl_description = "Stops the socket server."

    def execute(self, context):
        stop_server()
        return {'FINISHED'}

# Register and unregister classes
classes = (
    MOCAP_PT_Panel,
    MOCAP_OT_StartServer,
    MOCAP_OT_StopServer,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    print("Live Landmark Capture add-on registered.")

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    print("Live Landmark Capture add-on unregistered.")

if __name__ == "__main__":
    register()
