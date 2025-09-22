import json
import math

class Impactor:
    def __init__(self, radius_m, velocity_m_s, density_key, angle_deg, altitude_m=0):
        """
        radius_m   = impactor radius (m)
        velocity_m_s = impact velocity (m/s)
        density_key = which composition in constants.json (e.g. "Stony", "Iron")
        angle_deg  = impact angle from horizontal (degrees)
        altitude_m = entry altitude (default 0 = ground impact)
        """
        with open("constants.json", "rt") as file:
            self.constants = json.load(file)
        
        self.radius = radius_m
        self.velocity = velocity_m_s
        self.angle = math.radians(angle_deg)
        self.altitude = altitude_m
        
        # Pull density & strength
        comp = self.constants["IMPACTOR_COMPOSITIONS"][density_key]
        self.density = comp["density_kg_m3"]
        self.strength = comp["yield_strength_pa"]

        # Earth parameters
        self.g = self.constants["EARTH"]["gravity"]
        self.rho_air = self.constants["EARTH"]["air_density"]
        self.H = self.constants["EARTH"]["scale_height"]
        self.rho_target = self.constants["EARTH"]["target_density"]

    def mass(self):
        """Mass of impactor (kg)."""
        return (4/3) * math.pi * self.radius**3 * self.density

    def kinetic_energy(self):
        """Kinetic energy (Joules)."""
        return 0.5 * self.mass() * self.velocity**2

    def impactor_strength(self):
        """Check whether asteroid disrupts in atmosphere using dynamic pressure."""
        q = 0.5 * self.rho_air * self.velocity**2  # dynamic pressure
        return q >= self.strength  # True = breaks up

    def ground_impact_check(self):
        """Simple check if asteroid reaches ground before disruption."""
        # Atmospheric entry energy loss
        column_density = self.rho_air * self.H / math.sin(self.angle)
        threshold = self.density * self.radius
        return threshold > column_density  # True = survives to ground

    def transient_crater_diameter(self):
        """Pi-scaling crater diameter (m)."""
        E = self.kinetic_energy()
        g = self.g
        rho_t = self.rho_target
        rho_i = self.density

        # Holsapple scaling law (gravity regime)
        D = 1.161 * (rho_i/rho_t)**0.333 * (E/(rho_t * g))**0.25
        return D

    def thermal_exposure(self):
        """Thermal radiation exposure at ground (J/m^2)."""
        # Simplified: 10% KE converted to thermal, spread over fireball area
        E_th = 0.1 * self.kinetic_energy()
        R_fireball = 0.86 * (E_th)**(1/3.4)  # km scaling from Ahrens 1993
        A = 4 * math.pi * (R_fireball*1000)**2
        return E_th / A
    
    def fireball_radius(self):
        # Simplified: 10% KE converted to thermal, spread over fireball area
        E_th = 0.1 * self.kinetic_energy()
        R_fireball = 0.86 * (E_th)**(1/3.4)  # km scaling from Ahrens 1993
        return R_fireball*1000 # Convert to meter

    def air_blast(self, distance_m):
        """Scaled distance for air blast (Z)."""
        W = self.kinetic_energy() / (4.184e9)  # TNT equivalent (tons)
        Z = distance_m / (W**(1/3))  # scaled distance
        return Z

    def peak_overpressure(self, distance_m):
        """Peak overpressure at distance (Pa) using scaled distance law."""
        Z = self.air_blast(distance_m)
        # empirical law from nuclear blast scaling
        if Z < 0.3:
            P = 1e7  # cap at huge pressure near ground zero
        else:
            P = 8080 / (Z**3) + 114 / Z + 10  # kPa
            P *= 1000  # convert to Pa
        return P

    def richter_magnitude(self):
        """Seismic magnitude equivalent (Richter)."""
        E = self.kinetic_energy()
        # Gutenberg-Richter relation for explosion energy
        M = (2/3) * (math.log10(E) - 4.4)
        return M


if __name__ == "__main__":
    # Example test run
    imp = Impactor(
        radius_m=50,          # 50 m asteroid
        velocity_m_s=20000,   # 20 km/s
        density_key="Stony", 
        angle_deg=45
    )

    print("Mass (kg):", imp.mass())
    print("Kinetic Energy (J):", imp.kinetic_energy())
    print("Reaches Ground:", imp.ground_impact_check())
    print("Transient Crater Diameter (m):", imp.transient_crater_diameter())
    print("Thermal Exposure (J/m^2):", imp.thermal_exposure())
    print("Overpressure @10km (Pa):", imp.peak_overpressure(10000))
    print("Richter Magnitude:", imp.richter_magnitude())
