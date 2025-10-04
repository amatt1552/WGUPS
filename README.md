# WGUPS

This is a school project that calculates the most optimal route to deliver packages. I used a form of Nearest Neighbor algorithm, called pick_package, found in Truck, to deal with the order for delivery. The pick_package function requires another function to deliver and set the new current location, which is done in the deliver_package function, also found in Truck. Pick_package checks all packages in a truck and finds which has the closest deadline, then which destination is closer within that deadline. Deadline takes priority over distance, assuming something is not extremely close.

To run this project navigate to the WGUPS folder and type cmd in the address bar, then type python main.py into the cmd.

To start optimization first press the run button, then attempt to optimize afterwards with the optimize button.
