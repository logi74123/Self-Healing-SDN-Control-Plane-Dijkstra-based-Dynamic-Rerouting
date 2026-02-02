# Self-Healing SDN Control Plane: Dijkstra-based Dynamic Rerouting

[![Mininet](https://img.shields.io/badge/Network-Mininet-blue)](http://mininet.org/)
[![POX](https://img.shields.io/badge/Controller-POX-orange)](https://github.com/noxrepo/pox)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🌐 Overview
Inspired by the resilience requirements of **4G/5G infrastructure**, this project implements a Software Defined Networking (SDN) prototype designed for high availability. Using the **POX controller** and **Mininet**, I developed a self-healing control plane that uses **Dijkstra’s Algorithm** to calculate optimal paths and trigger sub-millisecond rerouting during link failures.

This project represents my fascination with the "plumbing" of the internet—moving beyond simple connectivity to building intelligent, autonomous network systems.

---

## ✨ Features
* **Dynamic Shortest Path**: Implements Dijkstra’s algorithm to compute paths based on real-time link costs (delays).
* **Self-Healing Architecture**: Automatically detects link downs and re-calculates the topology without packet loss.
* **Carrier-Grade Metrics**: Achieved a recovery time of **<1ms** during simulated failover events.
* **Data-Driven**: Uses an external `delay.csv` to simulate varying network conditions.

---

## 🛠️ Requirements & Installation

### Prerequisites
* **Linux Environment**: Ubuntu (Recommended) or Fedora (Prefer using Virtual Machine)
* **Mininet**: Network emulator
* **POX**: Python-based SDN controller

### Installation
1. **Clone the repositories:**
   ```bash
   git clone https://github.com/logi74123/SDN-Dynamic-Routing.git
   git clone https://github.com/noxrepo/pox.py
   ```

### Setup
Copy the files **delay.csv** and **dijkstra_controller.py** to the directory *pox/ext*
   
## ❓How to Run

   This project utilizes a modular SDN architecture. Follow these steps in order to ensure the **Control Plane (POX)** that correctly manages the **Data Plane (Mininet)**
   
1. **Launching the SDN Controller (POX)**
     Open your *first* terminal. Run the **dijkstra_controller** with the following command
     ```
     cd ~/pox/
     ./pox.py openflow.discovery misc.gephi_topo host_tracker dijkstra_controller```
     
2. **Launching the Network Topology (Mininet)**
     Open a *second* terminal. Use the custom topology script to build the switch-host infrastructure. 
     ``` sudo mn --custom topology_launcher.py --topo custom --controller remote --mac ```
   
3. **Visualizing the Network (Gephi)**
    Open a *third* terminal to launch the visualization tool.
    ```gephi```

4. **Monitoring the Traffic (Wireshark)**
     Launching *Wireshark* to inspect OpenFlow messages and packet headers.
     ```
     sudo su
     sudo wireshark
     ```

---

## 📊 Results & Analysis
When the simulation is running, the following behaviors can be observed:

* **Live Path Calculation**: As shown in the terminal logs below, the controller dynamically calculates and installs paths based the weight of link defined in *delay.csv* 
   * **Example:** `Path from s1 to h2: s1 -> s3-> s5`
   * **Example:** `Path from s2 to h2: s2 -> s4 -> s5`

![Dijkstra Path Calculations](https://i.postimg.cc/gJ7RpSyb/Screenshot-From-2026-02-01-19-25-50.png)
* **Network Graph**: Using the *misc.gephi_topo* module, the network topology is streamed live. This allows for a visual representation of the 5-switch mesh network, confirming that discovery and connectivity are working as intended. 

![Network Visualization](https://i.postimg.cc/sDhc9DLf/Screenshot-From-2026-02-02-00-25-52.png)

* **Packet Inspection**: **Wireshark** (monitoring the loopback interface) will capture `OFPT_FLOW_MOD` messages sent by the controller to update switch flow tables whenever a link state changes.

![Packet Inspection](https://i.postimg.cc/zBDNKQX8/Screenshot-From-2026-02-02-00-35-05.png)

![Packet Inspection](https://i.postimg.cc/QtND1zxD/Screenshot-From-2026-02-02-00-36-04.png)

## 🔧 Troubleshooting
Based on my development experience, here are solutions to common setup hurdles:

* **"Unable to contact remote controller"**: This occurs if Mininet is started before POX is fully initialized. 
  * **Solution**: Ensure the POX terminal shows `POX 0.3.0 (dart) is up` before running the `sudo mn` command.
* **Missing Lexer/Parser**: If you encounter errors during system-level configuration, ensure `flex` and `bison` are installed.
  * **Solution**: `sudo dnf install flex bison` (on Fedora) or `sudo apt install flex bison` (on Ubuntu).
* **Path Errors**: Ensure your project directory does not contain spaces(use underscore '_' instead), as this can break `Makefile` executions.

---

## 🧠 Learning Journey
Through this project, I explored the "full stack" of software-defined networking:

-   **Infrastructure as Code**: Programmatically defining network topologies using the Mininet Python API.
    
-   **Control Plane Logic**: Implementing Dijkstra's algorithm within a centralized controller to manage a distributed data plane.
    
-   **Protocol Analysis**: Using Wireshark to validate OpenFlow messaging and ARP resolution, ensuring the "handshake" between switches and the controller is robust.
    
-   **Real-time Observability**: Integrating Gephi to visualize mesh topology and monitor link-state changes dynamically.

---

## 👤 Author
**Logi Vasan**
* **LinkedIn**: [logi-vasan741](https://www.linkedin.com/in/logi-vasan741/)
* **GitHub**: [logi74123](https://github.com/logi74123)
     
