import math

def calculate_impact_consequences(L, rho_i_name, vi, theta, rho_t_name, r):
    """
    Calculates the consequences of an asteroid impact based on user-defined parameters.
    
    This function implements the core physics formulas and logic described in the
    user's provided document, including atmospheric entry and consequence modeling.

    Args:
        L (float): Projectile Diameter in meters.
        rho_i_name (str): Projectile Composition name (e.g., "Stony").
        vi (float): Impact Velocity in m/s.
        theta (float): Impact Angle in degrees.
        rho_t_name (str): Target Type name (e.g., "Rock").
        r (float): Distance from Impact in meters.
    """

    # --- 1. Required Variables and Constants ---
    
    # Material Lookups (from Impactor and Target tables)
    # The 'Impactor' lookup also includes a simplified material yield strength (Y).
    IMPACTOR_COMPOSITIONS = {
        "Stony": {"density_kg_m3": 2700, "yield_strength_pa": 1.0e6}, # Assumed yield strength
        "Iron": {"density_kg_m3": 7800, "yield_strength_pa": 1.0e8},  # Assumed yield strength
        "Carbonaceous": {"density_kg_m3": 1300, "yield_strength_pa": 1.0e5}, # Assumed yield strength
        "Comet": {"density_kg_m3": 920, "yield_strength_pa": 1.0e4}, # Assumed yield strength
    }
    
    TARGET_TYPES = {
        "Rock": {"density_kg_m3": 2700},
        "Water": {"density_kg_m3": 1000},
        "Sedimentary Rock": {"density_kg_m3": 2000},
    }
    
    # Constants
    g = 9.81  # Acceleration due to gravity in m/s²
    rho_0 = 1.225  # Atmospheric density at sea level in kg/m³
    KILOTON_TNT_JOULES = 4.184e12  # Conversion factor for energy from Joules to kilotons
    
    # --- 2. Core Physics Formulas (Modeling Sequence) ---
    
    try:
        # Get densities from lookups
        rho_i = IMPACTOR_COMPOSITIONS[rho_i_name]["density_kg_m3"]
        rho_t = TARGET_TYPES[rho_t_name]["density_kg_m3"]
        
        # Convert angle to radians for trigonometric functions
        theta_rad = math.radians(theta)
        
        # Stage 1 & 2: Energy, Strength, and Atmospheric Entry
        print("\n--- STAGE 1 & 2: Energy, Strength, and Atmospheric Entry ---")
        
        # Formula: Kinetic Energy (KE)
        # $KE = \frac{1}{2} m v_i^2$ where $m = \rho_i \cdot \frac{4}{3}\pi(\frac{L}{2})^3$
        m = rho_i * (4/3) * math.pi * (L/2)**3
        KE = 0.5 * m * vi**2
        print(f"Projectile Mass (m): {m:,.2f} kg")
        print(f"Total Kinetic Energy (KE): {KE:,.2e} Joules")
        
        # Formula: Impactor Strength (Yi)
        # Using the provided lookup, but we can also calculate it from a formula.
        # $log_{10}(Y_i) = 2.107 + 0.0624\rho_i$
        # Let's use the simplified yield strength from the lookup for this example.
        Y_i = IMPACTOR_COMPOSITIONS[rho_i_name]["yield_strength_pa"]
        print(f"Impactor Strength ($Y_i$): {Y_i:,.2e} Pascals")
        
        # Formula: Ground Impact Check
        # Condition: If $Y_i \ge \rho_0 v_i^2 \sin\theta$, Then: Ground Impact
        ground_impact_condition = rho_0 * vi**2 * math.sin(theta_rad)
        is_ground_impact = Y_i >= ground_impact_condition
        
        if is_ground_impact:
            print("Impact Result: The asteroid survives atmospheric entry and impacts the ground.")
            # --- Stage 3: Consequence Modeling (Ground Impact) ---
            print("\n--- STAGE 3: Consequence Modeling (Ground Impact) ---")
            
            # Formula: Transient Crater Diameter (Dtc)
            # $D_{tc} = 1.161(\frac{\rho_i}{\rho_t})^{1/3}L^{0.78}v_i^{0.44}g^{-0.22}(\sin\theta)^{1/3}$
            # The crater is formed by the remaining energy after atmospheric ablation, but for simplicity,
            # this formula uses the initial energy and adjusts for angle.
            Dtc = 1.161 * (rho_i / rho_t)**(1/3) * L**0.78 * vi**0.44 * g**-0.22 * (math.sin(theta_rad))**(1/3)
            print(f"Transient Crater Diameter ($D_{{tc}}$): {Dtc:,.2f} meters")
            
            # Formula: Richter Magnitude (M)
            # This is a simplified approximation from seismic data.
            # $M \approx 0.67 \log_{10}(E) - 5.87$
            M = 0.67 * math.log10(KE) - 5.87
            print(f"Richter Magnitude (M): {M:,.2f}")
            
        else:
            print("Impact Result: The asteroid explodes in an airburst.")
            # Adjust kinetic energy for airburst, assuming 50% is lost.
            # For this example, we'll use the full KE as the basis for the air blast.
            # Real models would account for energy loss during atmospheric entry.
            
        # These consequences apply to both ground impacts and airbursts.
        
        # Formula: Thermal Exposure (Φ)
        # $\Phi = \frac{\eta E}{2\pi r^2}$ where $\eta$ is the radiative coupling coefficient.
        # Assuming a coupling coefficient of 0.3 (common for airbursts).
        eta = 0.3
        Phi = (eta * KE) / (2 * math.pi * r**2)
        print(f"Thermal Exposure ($\Phi$) at {r} m: {Phi:,.2f} Joules/m²")
        
        # Formula: Air Blast (Scaled Distance) (r1)
        # $r_1 = \frac{r}{E_{kT}^{1/3}}$
        # Convert total energy to kilotons of TNT.
        E_kT = KE / KILOTON_TNT_JOULES
        r1 = r / (E_kT**(1/3))
        print(f"Scaled Distance ($r_1$): {r1:,.2f}")
        
        # Formula: Peak Overpressure (p)
        # $p \approx f(r_1, constants)$
        # Using a simplified approximation for peak overpressure in Pascals.
        # This formula is an approximation based on empirical data from nuclear explosions.
        p = 1000 * (0.01 + 0.5 * r1**-1.5 + 1.2 * r1**-3.2) if r1 > 0 else 0
        print(f"Peak Overpressure (p) at {r} m: {p:,.2f} Pascals")
        
    except KeyError as e:
        print(f"Error: Invalid material or target type. Please choose from the available options. {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Example Usage
if __name__ == "__main__":
    print("--- Asteroid Impact Simulation ---")
    
    # Example 1: A ground-impacting asteroid
    # Parameters for a large, stony asteroid hitting rock
    L_ex1 = 1000    # Projectile Diameter (1 km)
    rho_i_ex1 = "Stony" # Impactor Composition
    vi_ex1 = 20000  # Impact Velocity (20 km/s)
    theta_ex1 = 45  # Impact Angle (45 degrees)
    rho_t_ex1 = "Rock"  # Target Type
    r_ex1 = 50000   # Distance from Impact (50 km)
    
    print("\n--- Simulation 1: Stony Asteroid (Ground Impact) ---")
    calculate_impact_consequences(L_ex1, rho_i_ex1, vi_ex1, theta_ex1, rho_t_ex1, r_ex1)
    
    # Example 2: A smaller asteroid causing an airburst
    # Parameters for a smaller, cometary asteroid hitting water
    L_ex2 = 50    # Projectile Diameter (50 m)
    rho_i_ex2 = "Comet" # Impactor Composition
    vi_ex2 = 30000  # Impact Velocity (30 km/s)
    theta_ex2 = 25  # Impact Angle (25 degrees)
    rho_t_ex2 = "Water" # Target Type
    r_ex2 = 10000   # Distance from Impact (10 km)
    
    print("\n--- Simulation 2: Comet (Airburst) ---")
    calculate_impact_consequences(L_ex2, rho_i_ex2, vi_ex2, theta_ex2, rho_t_ex2, r_ex2)
    
    print("\n--- End of Simulation ---")