
CREATE TABLE frm_Address
(
	Street_Address_Ln_1  VARCHAR(125) NULL,
	City                 VARCHAR(64) NULL,
	ZIP_Code             VARCHAR(10) NULL,
	Address_ID           INTEGER AUTO_INCREMENT,
	Street_Address_Ln_2  VARCHAR(125) NULL,
	Effective_Date       DATE NULL,
	End_Date             DATE NULL,
	US_State_Code        CHAR(2) NULL,
	PRIMARY KEY (Address_ID)
) AUTO_INCREMENT = 1;



CREATE TABLE frm_Address_Info
(
	Address_Type         SMALLINT NOT NULL DEFAULT 0,
	Effective_Date       DATE NOT NULL,
	End_Date             DATE NULL,
	Comment              VARCHAR(255) NULL,
	Addressee_ID         INTEGER NOT NULL,
	Address_ID           INTEGER NOT NULL,
	Suite_Number         VARCHAR(3) NULL,
	Suite_Type_ID        INTEGER NULL,
	PRIMARY KEY (Address_Type,Effective_Date,Addressee_ID,Address_ID)
);



CREATE TABLE frn_Barrower_Business_Rlt
(
	Effective_Date       DATE NOT NULL,
	Deputy_Type_ID       CHAR(18) NULL DEFAULT 1,
	End_Date             DATE NULL,
	Borrower_ID          INTEGER NOT NULL,
	Business_ID          INTEGER NOT NULL,
	PRIMARY KEY (Effective_Date,Borrower_ID,Business_ID)
);



CREATE TABLE frn_Borrower
(
	Suffix               VARCHAR(5) NULL CHECK ( Suffix IN ('Ms.', 'Mr.', 'Mrs.', 'Dr.') ),
	First_Name           VARCHAR(30) NOT NULL,
	Middle_Name          VARCHAR(30) NULL,
	Last_Name            VARCHAR(30) NOT NULL,
	Date_of_Birth        DATE NOT NULL,
	Effective_Date       DATE NOT NULL,
	End_Date             DATE NULL,
	eMail_Address        VARCHAR(80) NULL,
	Home_Phone           VARCHAR(15) NULL,
	Cell_Phone           VARCHAR(15) NULL,
	SSN                  VARCHAR(11) NULL,
	Borrower_Status      CHAR(1) NOT NULL DEFAULT 1 CHECK ( Borrower_Status IN (1, 0, 2) ),
	Borrower_ID          INTEGER NOT NULL,
	PRIMARY KEY (Borrower_ID)
);



CREATE TABLE frn_Borrower_Bank_Account
(
	Business_ID          INTEGER NOT NULL,
	Bank_ID              INTEGER NOT NULL,
	Business_Bank_Account_ID INTEGER AUTO_INCREMENT,
	Account_Number       VARCHAR(10) NULL,
	Borrower_ID          INTEGER NULL,
	PRIMARY KEY (Business_Bank_Account_ID)
) AUTO_INCREMENT = 1;



CREATE TABLE frn_Borrower_Bank_Activity
(
	Trans_Date           DATE NULL,
	Trans_Amount         DECIMAL(18,2) NULL,
	Balance_Amount       DECIMAL(18,2) NULL,
	Business_Bank_Account_ID INTEGER NOT NULL,
	Trans_Type           SMALLINT NULL DEFAULT 0,
	Trans_ID             INTEGER AUTO_INCREMENT,
	Trans_Category_ID    INTEGER NULL,
	PRIMARY KEY (Trans_ID)
) AUTO_INCREMENT = 1;



CREATE TABLE frn_Business
(
	Business_Name        VARCHAR(30) NULL,
	DBA                  VARCHAR(30) NULL,
	Foundation_Date      DATE NULL,
	EIN                  VARCHAR(11) NULL,
	Risk_Category        CHAR(1) NULL,
	Business_ID          INTEGER AUTO_INCREMENT,
	Incorparation_State_Code CHAR(2) NULL,
	Business_Phone       VARCHAR(15) NULL,
	Effective_Date       DATE NOT NULL,
	End_Date             DATE NULL,
	Legal_Form_Type_ID   INTEGER NULL,
	Industry_Type_ID     INTEGER NULL,
	PRIMARY KEY (Business_ID)
) AUTO_INCREMENT = 1;



CREATE TABLE frn_Business_Measure
(
	Business_ID          INTEGER NOT NULL,
	Measure_Date         DATE NOT NULL,
	Monthly_Sale_Amount  DECIMAL(18,2) NULL,
	Previous_Year_Revenue DECIMAL(18,2) NULL,
	Previous_Year_Net_Profit DECIMAL(18,2) NULL,
	PRIMARY KEY (Business_ID,Measure_Date)
);



CREATE TABLE frn_Fin_Institution
(
	Fin_Institution_ID   INTEGER AUTO_INCREMENT,
	Fin_Institution_Name VARCHAR(30) NULL,
	Effective_Date       DATE NULL,
	End_Date             DATE NULL,
	Fin_Institution_Type_ID INTEGER NULL,
	Incorparation_State_Code CHAR(2) NULL,
	Fin_Institution_Code VARCHAR(5) NULL,
	Routing_Number       VARCHAR(10) NULL,
	PRIMARY KEY (Fin_Institution_ID)
) AUTO_INCREMENT = 1;



CREATE TABLE frn_Fin_Institution_Type
(
	Fin_Institution_Type_ID INTEGER AUTO_INCREMENT,
	Fin_Institution_Type_Name VARCHAR(30) NULL,
	Fin_Institution_Type_Desc VARCHAR(125) NULL,
	PRIMARY KEY (Fin_Institution_Type_ID)
) AUTO_INCREMENT = 1;



CREATE TABLE frn_Industry_Type
(
	Industry_Type_ID     INTEGER AUTO_INCREMENT,
	Industry_Type_Name   VARCHAR(30) NULL,
	Industry_Type_Description VARCHAR(125) NULL,
	NAICS_code           VARCHAR(10) NULL,
	SIC_Code             VARCHAR(10) NULL,
	PRIMARY KEY (Industry_Type_ID)
) AUTO_INCREMENT = 1;



CREATE TABLE frn_Legal_Form_Type
(
	Legal_Form_Type_ID   INTEGER AUTO_INCREMENT,
	Legal_Form_Name      VARCHAR(30) NULL,
	Legal_Form_Desc      VARCHAR(125) NULL,
	PRIMARY KEY (Legal_Form_Type_ID)
) AUTO_INCREMENT = 1;



CREATE TABLE frn_Lender
(
	Suffix               VARCHAR(5) NULL CHECK ( Suffix IN (1, 0, 2) ),
	First_Name           VARCHAR(30) NOT NULL,
	Middle_Name          VARCHAR(30) NULL,
	Last_Name            VARCHAR(30) NOT NULL,
	Effective_Date       DATE NOT NULL,
	End_Date             DATE NULL,
	Lender_ID            INTEGER NOT NULL,
	Work_Phone           VARCHAR(15) NULL,
	Cell_Phone           VARCHAR(15) NULL,
	Lender_Status        CHAR(1) NOT NULL DEFAULT 1 CHECK ( Lender_Status IN (1, 0, 2) ),
	PRIMARY KEY (Lender_ID)
);



CREATE TABLE frn_Lender_Fin_Institution_Rlt
(
	Fin_Institution_ID   INTEGER NOT NULL,
	Effective_Date       DATE NOT NULL,
	End_Date             DATE NULL,
	Lender_ID            INTEGER NOT NULL,
	PRIMARY KEY (Fin_Institution_ID,Effective_Date,Lender_ID)
);



CREATE TABLE frn_Loan_Offer
(
	Loan_Offer_ID        INTEGER AUTO_INCREMENT,
	Amount               CHAR(18) NULL,
	Discount             CHAR(18) NULL,
	Offer_Date           CHAR(18) NULL,
	Offer_Exp_Date       CHAR(18) NULL,
	Repaid_Amount        CHAR(18) NULL,
	Estimated_Repaid_Term CHAR(18) NULL,
	Daily_Repeyment_Sale_Percent CHAR(18) NULL,
	Status               CHAR(18) NULL DEFAULT 99,
	Status_Change_Date   CHAR(18) NULL,
	Borrower_ID          INTEGER NULL,
	Lender_ID            INTEGER NULL,
	Fin_Institution_ID   INTEGER NULL,
	PRIMARY KEY (Loan_Offer_ID)
) AUTO_INCREMENT = 1;



CREATE TABLE frn_Loan_Request
(
	Request_Date         DATE NULL,
	Loan_Amount          DECIMAL(18,2) NULL,
	Loan_Request_ID      INTEGER AUTO_INCREMENT,
	Business_ID          INTEGER NULL,
	Borrower_ID          INTEGER NULL,
	PRIMARY KEY (Loan_Request_ID)
) AUTO_INCREMENT = 1;



CREATE TABLE frn_Request_Business_Measure
(
	Loan_Request_ID      INTEGER NOT NULL,
	Business_ID          INTEGER NOT NULL,
	Measure_Date         DATE NOT NULL,
	PRIMARY KEY (Loan_Request_ID,Business_ID,Measure_Date)
);



CREATE TABLE frn_Suite_Type
(
	Suite_Type_ID        INTEGER AUTO_INCREMENT,
	Suite_Type_Name      VARCHAR(30) NULL,
	Suite_Type_Desc      VARCHAR(125) NULL,
	PRIMARY KEY (Suite_Type_ID)
) AUTO_INCREMENT = 1;



CREATE TABLE frn_System_Account
(
	EMmail               VARCHAR(80) NOT NULL,
	Password             VARCHAR(255) NOT NULL,
	System_Account_ID    INTEGER AUTO_INCREMENT,
	Status               CHAR(1) NOT NULL CHECK ( Status IN (1, 0, 2) ),
	Account_Type         CHAR(1) NOT NULL CHECK ( Account_Type IN (0, 1) ),
	Effective_Date       DATE NOT NULL,
	End_Date             DATE NULL,
	PRIMARY KEY (System_Account_ID)
) AUTO_INCREMENT = 1;



CREATE TABLE frn_Trans_Category
(
	Trans_Category_ID    INTEGER AUTO_INCREMENT,
	Trans_Category_Name  VARCHAR(30) NULL,
	Trans_Category_Desc  VARCHAR(125) NULL,
	PRIMARY KEY (Trans_Category_ID)
) AUTO_INCREMENT = 1;



CREATE TABLE frn_US_State
(
	US_State_Name        VARCHAR(30) NULL,
	US_State_Code        CHAR(2) NOT NULL,
	PRIMARY KEY (US_State_Code)
);



ALTER TABLE frm_Address
ADD FOREIGN KEY R_94 (US_State_Code) REFERENCES frn_US_State (US_State_Code);



ALTER TABLE frm_Address_Info
ADD FOREIGN KEY R_65 (Addressee_ID) REFERENCES frn_Lender (Lender_ID);



ALTER TABLE frm_Address_Info
ADD FOREIGN KEY R_66 (Addressee_ID) REFERENCES frn_Business (Business_ID);



ALTER TABLE frm_Address_Info
ADD FOREIGN KEY R_67 (Address_ID) REFERENCES frm_Address (Address_ID);



ALTER TABLE frm_Address_Info
ADD FOREIGN KEY R_75 (Suite_Type_ID) REFERENCES frn_Suite_Type (Suite_Type_ID);



ALTER TABLE frm_Address_Info
ADD FOREIGN KEY R_76 (Addressee_ID) REFERENCES frn_Fin_Institution (Fin_Institution_ID);



ALTER TABLE frn_Barrower_Business_Rlt
ADD FOREIGN KEY R_42 (Borrower_ID) REFERENCES frn_Borrower (Borrower_ID);



ALTER TABLE frn_Barrower_Business_Rlt
ADD FOREIGN KEY R_47 (Business_ID) REFERENCES frn_Business (Business_ID);



ALTER TABLE frn_Borrower
ADD FOREIGN KEY R_39 (Borrower_ID) REFERENCES frn_System_Account (System_Account_ID);



ALTER TABLE frn_Borrower_Bank_Account
ADD FOREIGN KEY R_79 (Business_ID) REFERENCES frn_Business (Business_ID);



ALTER TABLE frn_Borrower_Bank_Account
ADD FOREIGN KEY R_81 (Bank_ID) REFERENCES frn_Fin_Institution (Fin_Institution_ID);



ALTER TABLE frn_Borrower_Bank_Account
ADD FOREIGN KEY R_86 (Borrower_ID) REFERENCES frn_Borrower (Borrower_ID);



ALTER TABLE frn_Borrower_Bank_Activity
ADD FOREIGN KEY R_82 (Business_Bank_Account_ID) REFERENCES frn_Borrower_Bank_Account (Business_Bank_Account_ID);



ALTER TABLE frn_Borrower_Bank_Activity
ADD FOREIGN KEY R_93 (Trans_Category_ID) REFERENCES frn_Trans_Category (Trans_Category_ID);



ALTER TABLE frn_Business
ADD FOREIGN KEY R_46 (Incorparation_State_Code) REFERENCES frn_US_State (US_State_Code);



ALTER TABLE frn_Business
ADD FOREIGN KEY R_69 (Legal_Form_Type_ID) REFERENCES frn_Legal_Form_Type (Legal_Form_Type_ID);



ALTER TABLE frn_Business
ADD FOREIGN KEY R_70 (Industry_Type_ID) REFERENCES frn_Industry_Type (Industry_Type_ID);



ALTER TABLE frn_Business_Measure
ADD FOREIGN KEY R_60 (Business_ID) REFERENCES frn_Business (Business_ID);



ALTER TABLE frn_Fin_Institution
ADD FOREIGN KEY R_74 (Fin_Institution_Type_ID) REFERENCES frn_Fin_Institution_Type (Fin_Institution_Type_ID);



ALTER TABLE frn_Fin_Institution
ADD FOREIGN KEY R_78 (Incorparation_State_Code) REFERENCES frn_US_State (US_State_Code);



ALTER TABLE frn_Lender
ADD FOREIGN KEY R_40 (Lender_ID) REFERENCES frn_System_Account (System_Account_ID);



ALTER TABLE frn_Lender_Fin_Institution_Rlt
ADD FOREIGN KEY R_10 (Fin_Institution_ID) REFERENCES frn_Fin_Institution (Fin_Institution_ID);



ALTER TABLE frn_Lender_Fin_Institution_Rlt
ADD FOREIGN KEY R_50 (Lender_ID) REFERENCES frn_Lender (Lender_ID);



ALTER TABLE frn_Loan_Offer
ADD FOREIGN KEY R_83 (Borrower_ID) REFERENCES frn_Borrower (Borrower_ID);



ALTER TABLE frn_Loan_Offer
ADD FOREIGN KEY R_84 (Lender_ID) REFERENCES frn_Lender (Lender_ID);



ALTER TABLE frn_Loan_Offer
ADD FOREIGN KEY R_85 (Fin_Institution_ID) REFERENCES frn_Fin_Institution (Fin_Institution_ID);



ALTER TABLE frn_Loan_Request
ADD FOREIGN KEY R_59 (Business_ID) REFERENCES frn_Business (Business_ID);



ALTER TABLE frn_Loan_Request
ADD FOREIGN KEY R_64 (Borrower_ID) REFERENCES frn_Borrower (Borrower_ID);



ALTER TABLE frn_Request_Business_Measure
ADD FOREIGN KEY R_61 (Loan_Request_ID) REFERENCES frn_Loan_Request (Loan_Request_ID);



ALTER TABLE frn_Request_Business_Measure
ADD FOREIGN KEY R_63 (Business_ID, Measure_Date) REFERENCES frn_Business_Measure (Business_ID, Measure_Date);


