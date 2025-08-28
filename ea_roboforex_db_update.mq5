//+------------------------------------------------------------------+
//| RoboForex Status Update Code für don_gpt.mq5                    |
//| Füge diesen Code in OnInit() ein                                |
//+------------------------------------------------------------------+

// Diese Funktion sollte in OnInit() aufgerufen werden
void UpdateRoboForexStatusInDB()
{
    // Hole Account-Informationen
    string accountNumber = IntegerToString(AccountInfoInteger(ACCOUNT_LOGIN));
    string brokerName = AccountInfoString(ACCOUNT_COMPANY);
    
    // Prüfe RoboForex Partner Status
    bool isPartner = false;
    string roboStatus = "no";
    
    if(UseRoboForexCheck)
    {
        // Prüfe ob es ein RoboForex Broker ist
        if(StringFind(brokerName, "RoboForex") >= 0 || 
           StringFind(brokerName, "RoboMarkets") >= 0)
        {
            // Prüfe Partner-Status
            isPartner = CheckRoboForexLicense();
            roboStatus = isPartner ? "yes" : "no";
            
            Print("RoboForex Partner Status: ", roboStatus);
        }
        else
        {
            Print("Kein RoboForex Broker - Status Update übersprungen");
            return;
        }
    }
    
    // Sende Status an Server
    SendRoboStatusToServer(accountNumber, roboStatus);
}

//+------------------------------------------------------------------+
//| Sende RoboForex Status an Server                                |
//+------------------------------------------------------------------+
void SendRoboStatusToServer(string accountNumber, string roboStatus)
{
    Print("Sende RoboForex Status an Server...");
    
    // Erstelle URL für Status Update
    string url = "https://" + DOMEN + "/files/update_robo_status.php";
    
    // Erstelle POST Data
    string postData = "account=" + accountNumber + 
                     "&robo_status=" + roboStatus +
                     "&program=" + PROGRAM_NAME +
                     "&api_key=" + ROBOFOREX_API_KEY;
    
    // Verwende WebRequest
    char post[], result[];
    string headers = "Content-Type: application/x-www-form-urlencoded\r\n";
    
    StringToCharArray(postData, post, 0, StringLen(postData));
    
    int res = WebRequest("POST", url, headers, 5000, post, result, headers);
    
    if(res > 0)
    {
        string response = CharArrayToString(result);
        Print("Server Response: ", response);
        
        if(StringFind(response, "success") >= 0)
        {
            Print("✓ RoboForex Status erfolgreich aktualisiert: ", roboStatus);
        }
        else
        {
            Print("⚠ Server Update fehlgeschlagen: ", response);
        }
    }
    else
    {
        Print("✗ WebRequest fehlgeschlagen. Error: ", GetLastError());
        
        // Alternative: Verwende WinInet
        UpdateViaWinInet(accountNumber, roboStatus);
    }
}

//+------------------------------------------------------------------+
//| Alternative Update via WinInet                                  |
//+------------------------------------------------------------------+
void UpdateViaWinInet(string accountNumber, string roboStatus)
{
    Print("Verwende WinInet für Status Update...");
    
    int hSession = InternetOpenW("DAX_EA", 1, NULL, NULL, 0);
    if(hSession == 0)
    {
        Print("✗ InternetOpen fehlgeschlagen");
        return;
    }
    
    int hConnect = InternetConnectW(hSession, DOMEN, serverPort, 
                                    NULL, NULL, 3, 0, 0);
    if(hConnect == 0)
    {
        InternetCloseHandle(hSession);
        Print("✗ InternetConnect fehlgeschlagen");
        return;
    }
    
    // Erstelle Request Path mit Parametern
    string path = "/files/update_robo_status.php?" +
                 "account=" + accountNumber + 
                 "&robo_status=" + roboStatus +
                 "&program=" + PROGRAM_NAME;
    
    int hRequest = HttpOpenRequestW(hConnect, "GET", path, 
                                    NULL, NULL, NULL, 
                                    0x84800200, 0); // HTTPS Flags
    
    if(hRequest == 0)
    {
        InternetCloseHandle(hConnect);
        InternetCloseHandle(hSession);
        Print("✗ HttpOpenRequest fehlgeschlagen");
        return;
    }
    
    if(HttpSendRequestW(hRequest, NULL, 0, NULL, 0))
    {
        char buffer[1024];
        uint bytesRead = 0;
        
        if(InternetReadFile(hRequest, buffer, 1024, bytesRead))
        {
            string response = CharArrayToString(buffer, 0, bytesRead);
            Print("WinInet Response: ", response);
            
            if(StringFind(response, "success") >= 0)
            {
                Print("✓ Status via WinInet aktualisiert");
            }
        }
    }
    else
    {
        Print("✗ HttpSendRequest fehlgeschlagen");
    }
    
    InternetCloseHandle(hRequest);
    InternetCloseHandle(hConnect);
    InternetCloseHandle(hSession);
}

//+------------------------------------------------------------------+
//| Erweiterte OnInit() Funktion                                    |
//| Füge diese Zeilen in die bestehende OnInit() ein               |
//+------------------------------------------------------------------+

// In OnInit() nach der Lizenzprüfung hinzufügen:

    // Update RoboForex Status in Database
    if(!MQLInfoInteger(MQL_TESTER))  // Nicht im Backtest
    {
        UpdateRoboForexStatusInDB();
    }

//+------------------------------------------------------------------+
//| PHP Script für Server (update_robo_status.php)                  |
//+------------------------------------------------------------------+
/*
Erstelle diese PHP-Datei auf dem Server:

<?php
// update_robo_status.php
// Aktualisiert den RoboForex Status in der Datenbank

// Database Configuration
$db_host = '162.55.90.123';
$db_user = 'prophelper';
$db_pass = '.Propt333doka?';
$db_name = 'prophelper';

// Get Parameters
$account = isset($_REQUEST['account']) ? $_REQUEST['account'] : '';
$robo_status = isset($_REQUEST['robo_status']) ? $_REQUEST['robo_status'] : 'no';
$program = isset($_REQUEST['program']) ? $_REQUEST['program'] : '';
$api_key = isset($_REQUEST['api_key']) ? $_REQUEST['api_key'] : '';

// Validate
if(empty($account)) {
    die('error: no account number');
}

// Validate API Key (optional)
$expected_key = 'ec4d40c4343ee741';
if($api_key != $expected_key) {
    die('error: invalid api key');
}

// Connect to database
$conn = new mysqli($db_host, $db_user, $db_pass, $db_name);

if($conn->connect_error) {
    die('error: database connection failed');
}

// Update roboaffiliate status
$sql = "UPDATE lnative SET roboaffiliate = ? 
        WHERE (accountLogin = ? OR account = ?)";

if($program) {
    $sql .= " AND program = ?";
}

$stmt = $conn->prepare($sql);

if($program) {
    $stmt->bind_param("ssss", $robo_status, $account, $account, $program);
} else {
    $stmt->bind_param("sss", $robo_status, $account, $account);
}

if($stmt->execute()) {
    if($stmt->affected_rows > 0) {
        echo "success: updated " . $stmt->affected_rows . " rows";
    } else {
        echo "success: no rows updated (account not found or status unchanged)";
    }
} else {
    echo "error: update failed";
}

$stmt->close();
$conn->close();
?>
*/