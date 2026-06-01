# HITL & SIH on Pixhawk 6c with Jetson Orin Nano

Robotics Industry has been under rapid development. One of the main areas is advancement in Simulation technologies which is more well known as Digital-Twins.
Engineering materials and devices require advance technical skills which make it hard to be build all over the world. So there are certain countries which can make High-end devices like Flight Controllers, Sensors, Cameras better and cheaper like India or China.
Hence, simulation practices are used to speed up the development process even if required parts is not present. Additionally, risking these hard gained materials in trials can lead to high R&D cost for companies and prevent small businesses to be able to compete.

In the drone industry, SITL (Software-In-The-Loop) and SIH (Simulation-In-Hardware) are virtual testing environments used to validate autopilot software and algorithms without risking physical hardware. Both are heavily featured in development blogs to highlight crash-free coding and algorithm validation. 
Key Differences in Testing Methodologies

    SITL (Software-In-The-Loop): The flight control firmware (e.g., ArduPilot or PX4) runs directly as a compiled program on your desktop or laptop. It communicates with a 3D visualization simulator (like Gazebo or FlightGear) to mimic flight physics, sensors, and GPS. It is the industry-standard first step for debugging code safely.
    SIH (Simulation-In-Hardware): This is a stripped-down, lightweight simulation mode where a basic physics engine is loaded directly onto the actual drone's flight controller (e.g., a Pixhawk or Cube Orange). It allows developers to test how the physical board processes telemetry and sensor data without needing the drone to physically fly. 

Typical Use Cases in Development

    Early-Stage Logic: Developers rely on SITL to write and test autonomous flight paths, obstacle avoidance, and computer vision algorithms before ever touching a real airframe.
    Hardware Debugging: Industry blogs show engineers using SIH to verify electrical I/O timings, check flash memory loads, and validate remote controller inputs to the physical autopilot.
    Cost Efficiency: Both methods save development teams time and budget by preventing crashes during the experimental testing phases. 

SIH runs as a PX4 module that replaces real sensor and actuator hardware with a simulated physics model. It provides simulated IMU, GPS, barometer, magnetometer, and airspeed sensor data via uORB, and reads actuator outputs to update the vehicle state at each timestep.The simulation runs in lockstep with PX4, ensuring deterministic and reproducible results.

Alternatively, SITL is also commonly used for testing out drone apps running on python. For these apps, the drone firmware isn’t changed.  These high level apps leave the low level firmware unchanged, and focus on moving the drone in new and unique ways. This could be either delivery mission, object recognition, or any other drone app you can think of.
