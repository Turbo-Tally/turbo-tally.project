

# list of regions
regions = [
    { "name": "NCR", "long": "National Capital Region", "key": "NCR" },
    { "name": "CAR", "long": "Cordillera Admininstrative Region", "key": "CAR" },
    { "name": "Region I", "long": "Ilocos Region", "key": "I" },
    { "name": "Region II", "long": "Cagayan Valley", "key": "II" },
    { "name": "Region III", "long": "Central Luzon", "key": "III" },
    { "name": "Region IV-A", "long": "CALABARZON", "key": "IV-A" },
    { "name": "Region IV-B", "long": "MIMAROPA", "key": "IV-B" },
    { "name": "Region V", "long": "Bicol Region", "key": "V" },
    { "name": "Region VI", "long": "Western Visayas", "key": "VI" },
    { "name": "Region VII", "long": "Central Visayas", "key": "VII" },
    { "name": "Region VIII", "long": "Eastern Visayas", "key": "VIII" },
    { "name": "Region IX", "long": "Zamboange Peninsula", "key": "IX" },
    { "name": "Region X", "long": "Northern Mindanao", "key": "X" },
    { "name": "Region XI", "long": "Davao Region", "key": "XI" },
    { "name": "Region XII", "long": "SOCCSKARGEN", "key": "XII" },
    { "name": "Region XIII", "long": "Caraga", "key": "XIII" },
    { "name": "ARMM", "long": "Autonomous Region in Muslim Mindanao", "key": "ARMM" }
]

# list of provinces 
provinces = [
  { "name": "Metro Manila", "region": "NCR", "key": "MM" },

  { "name": "Abra", "region": "CAR", "key": "ABR" },
  { "name": "Apayao", "region": "CAR", "key": "APA" },
  { "name": "Benguet", "region": "CAR", "key": "BEN" },
  { "name": "Ifugao", "region": "CAR", "key": "IFU" },
  { "name": "Kalinga", "region": "CAR", "key": "KAL" },
  { "name": "Mountain Province", "region": "CAR", "key": "MOU" },

  { "name": "Ilocos Norte", "region": "I", "key": "ILN" },
  { "name": "Ilocos Sur", "region": "I", "key": "ILS" },
  { "name": "La Union", "region": "I", "key": "LUN" },
  { "name": "Pangasinan", "region": "I", "key": "PAN" },

  { "name": "Batanes", "region": "II", "key": "BTN" },
  { "name": "Cagayan", "region": "II", "key": "CAG" },
  { "name": "Isabela", "region": "II", "key": "ISA" },
  { "name": "Nueva Vizcaya", "region": "II", "key": "NUV" },
  { "name": "Quirino", "region": "II", "key": "QUI" },

  { "name": "Aurora", "region": "III", "key": "AUR" },
  { "name": "Bataan", "region": "III", "key": "BAN" },
  { "name": "Bulacan", "region": "III", "key": "BUL" },
  { "name": "Nueva Ecija", "region": "III", "key": "NUE" },
  { "name": "Pampanga", "region": "III", "key": "PAM" },
  { "name": "Tarlac", "region": "III", "key": "TAR" },
  { "name": "Zambales", "region": "III", "key": "ZMB" },

  { "name": "Batangas", "region": "IV-A", "key": "BTG" },
  { "name": "Cavite", "region": "IV-A", "key": "CAV" },
  { "name": "Laguna", "region": "IV-A", "key": "LAG" },
  { "name": "Quezon", "region": "IV-A", "key": "QUE" },
  { "name": "Rizal", "region": "IV-A", "key": "RIZ" },

  { "name": "Marinduque", "region": "IV-B", "key": "MAD" },
  { "name": "Occidental Mindoro", "region": "IV-B", "key": "MDC" },
  { "name": "Oriental Mindoro", "region": "IV-B", "key": "MDR" },
  { "name": "Palawan", "region": "IV-B", "key": "PLW" },
  { "name": "Romblon", "region": "IV-B", "key": "ROM" },

  { "name": "Albay", "region": "V", "key": "ALB" },
  { "name": "Camarines Norte", "region": "V", "key": "CAN" },
  { "name": "Camarines Sur", "region": "V", "key": "CAS" },
  { "name": "Catanduanes", "region": "V", "key": "CAT" },
  { "name": "Masbate", "region": "V", "key": "MAS" },
  { "name": "Sorsogon", "region": "V", "key": "SOR" }, 

  { "name": "Aklan", "region": "VI", "key": "AKL" },
  { "name": "Antique", "region": "VI", "key": "ANT" },
  { "name": "Capiz", "region": "VI", "key": "CAP" },
  { "name": "Guimaras", "region": "VI", "key": "GUI" },
  { "name": "Iloilo", "region": "VI", "key": "ILI" },
  { "name": "Negros Occidental", "region": "VI", "key": "NEC" },

  { "name": "Bohol", "region": "VII", "key": "BOH" },
  { "name": "Cebu", "region": "VII", "key": "CEB" },
  { "name": "Negros Oriental", "region": "VII", "key": "NER" },
  { "name": "Siquijor", "region": "VII", "key": "SIG" },

  { "name": "Biliran", "region": "VIII", "key": "BIL" },
  { "name": "Eastern Samar", "region": "VIII", "key": "EAS" },
  { "name": "Leyte", "region": "VIII", "key": "LEY" },
  { "name": "Northern Samar", "region": "VIII", "key": "NSA" },
  { "name": "Samar", "region": "VIII", "key": "WSA" },
  { "name": "Southern Leyte", "region": "VIII", "key": "SLE" },

  { "name": "Zamboanga del Norte", "region": "IX", "key": "ZAN" },
  { "name": "Zamboanga del Sur", "region": "IX", "key": "ZAS" },
  { "name": "Zamboanga Sibugay", "region": "IX", "key": "ZSI" },

  { "name": "Bukidnon", "region": "X", "key": "BUK" },
  { "name": "Camiguin", "region": "X", "key": "CAM" },
  { "name": "Lanao del Norte", "region": "X", "key": "LAN" },
  { "name": "Misamis Occidental", "region": "X", "key": "MSC" },
  { "name": "Misamis Oriental", "region": "X", "key": "MSR" },

  { "name": "Compostela Valley", "region": "XI", "key": "COM" },
  { "name": "Davao del Norte", "region": "XI", "key": "DAV" },
  { "name": "Davao del Sur", "region": "XI", "key": "DAS" },
  { "name": "Davao Occidental", "region": "XI", "key": "DAC" },
  { "name": "Davao Oriental", "region": "XI", "key": "DAO" },

  { "name": "Cotabato", "region": "XII", "key": "NCO" },
  { "name": "Sarangani", "region": "XII", "key": "SAR" },
  { "name": "South Cotabato", "region": "XII", "key": "SCO" },
  { "name": "Sultan Kudarat", "region": "XII", "key": "SUK" },

  { "name": "Agusan del Norte", "region": "XIII", "key": "AGN" },
  { "name": "Agusan del Sur", "region": "XIII", "key": "AGS" },
  { "name": "Dinagat Islands", "region": "XIII", "key": "DIN" },
  { "name": "Surigao del Norte", "region": "XIII", "key": "SUN" },
  { "name": "Surigao del Sur", "region": "XIII", "key": "SUR" },

  { "name": "Basilan", "region": "ARMM", "key": "BAS" },
  { "name": "Lanao del Sur", "region": "ARMM", "key": "LAS" },
  { "name": "Maguindanao", "region": "ARMM", "key": "MAG" },
  { "name": "Sulu", "region": "ARMM", "key": "SLU" },
  { "name": "Tawi-tawi", "region": "ARMM", "key": "TAW" }
]