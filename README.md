# event-management-system


        +--------------------+      Schedules     +-------------------+
        |      Patient       |-------------------|    Appointment    |
        |--------------------|   (1:M)            |-------------------|
        | Patient_ID (PK)    |                   | Appointment_ID (PK)|
        | Name               |                   | Date               |
        | Age                |                   | Time               |
        | Gender             |                   | Patient_ID (FK)    |
        | Address            |                   | Doctor_ID (FK)     |
        | Contact            |                   +-------------------+
        | Medical_History    |
        +--------------------+
              | (1:M)
              |
   Has       |        +------------------+
  (1:M)      |        |      Doctor      |
              --------|------------------|
                       | Doctor_ID (PK)  |
                       | Name            |
                       | Specialization  |
                       | Experience      |
                       | Department      |
                       +------------------+

                       | (1:M)
                       |
                       | Creates
                       | (1:M)
        +-------------------------+
        |    Medical Record       |
        |-------------------------|
        | Record_ID (PK)          |
        | Patient_ID (FK)         |
        | Doctor_ID (FK)          |
        | Diagnosis               |
        | Prescriptions           |
        +-------------------------+

                       | (1:M)
                       |
                       | Pays for
                       | (1:M)
        +-------------------------+
        |       Billing           |
        |-------------------------|
        | Bill_ID (PK)            |
        | Patient_ID (FK)         |
        | Total Cost              |
        | Payment Status          |
        +-------------------------+
