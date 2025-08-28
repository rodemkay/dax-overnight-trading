#!/usr/bin/env python3
"""
Modifiziert die template.inc.php um die RoboForex Partner-Spalte hinzuzufügen
"""

import re

def modify_template(input_file, output_file):
    """Fügt die RoboForex-Spalte zur template.inc.php hinzu"""
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("✓ Original-Datei gelesen")
    
    # 1. Erweitere den ersten SELECT um roboaffiliate
    old_select = "SELECT full_name,program,test,ip,serialNo FROM `lnative`"
    new_select = "SELECT full_name,program,test,ip,serialNo,roboaffiliate FROM `lnative`"
    content = content.replace(old_select, new_select)
    print("✓ SELECT-Query erweitert")
    
    # 2. Füge Sort-Option für RoboForex hinzu (nach IP, vor den Trennlinien)
    old_sort_options = """<option value="11" <?=$sort==11?"selected":''?>>IP</option>
	<option disabled="disabled">- - - - - - - - -</option>"""
    new_sort_options = """<option value="11" <?=$sort==11?"selected":''?>>IP</option>
	<option value="13" <?=$sort==13?"selected":''?>>RoboForex Partner</option>
	<option disabled="disabled">- - - - - - - - -</option>"""
    content = content.replace(old_sort_options, new_sort_options)
    print("✓ Sort-Option hinzugefügt")
    
    # 3. Füge Sort-Query für roboaffiliate hinzu (ASC Sortierung)
    # Nach sort==12 und vor sort==14
    old_sort_asc = """if($sort==12) $result = mysqli_query($db,"SELECT * FROM `lnative` WHERE `test`='$url' AND `program`='$program' ORDER BY `full_name_blocked` DESC, full_name ASC LIMIT $offset, $limit");
if($sort==14) $result = mysqli_query($db,"SELECT * FROM `lnative` WHERE `test`='$url' AND `program`='$program' ORDER BY `serialNo_blocked` DESC, serialNo ASC LIMIT $offset, $limit");"""
    new_sort_asc = """if($sort==12) $result = mysqli_query($db,"SELECT * FROM `lnative` WHERE `test`='$url' AND `program`='$program' ORDER BY `full_name_blocked` DESC, full_name ASC LIMIT $offset, $limit");
if($sort==13) $result = mysqli_query($db,"SELECT * FROM `lnative` WHERE `test`='$url' AND `program`='$program' ORDER BY `roboaffiliate` DESC LIMIT $offset, $limit");
if($sort==14) $result = mysqli_query($db,"SELECT * FROM `lnative` WHERE `test`='$url' AND `program`='$program' ORDER BY `serialNo_blocked` DESC, serialNo ASC LIMIT $offset, $limit");"""
    content = content.replace(old_sort_asc, new_sort_asc)
    
    # DESC Sortierung
    old_sort_desc = """if($sort==12) $result = mysqli_query($db,"SELECT * FROM `lnative` WHERE `test`='$url' AND `program`='$program' ORDER BY `full_name_blocked` DESC, full_name ASC LIMIT $offset, $limit");
if($sort==14) $result = mysqli_query($db,"SELECT * FROM `lnative` WHERE `test`='$url' AND `program`='$program' ORDER BY `serialNo_blocked` DESC, serialNo ASC LIMIT $offset, $limit");"""
    new_sort_desc = """if($sort==12) $result = mysqli_query($db,"SELECT * FROM `lnative` WHERE `test`='$url' AND `program`='$program' ORDER BY `full_name_blocked` DESC, full_name ASC LIMIT $offset, $limit");
if($sort==13) $result = mysqli_query($db,"SELECT * FROM `lnative` WHERE `test`='$url' AND `program`='$program' ORDER BY `roboaffiliate` DESC LIMIT $offset, $limit");
if($sort==14) $result = mysqli_query($db,"SELECT * FROM `lnative` WHERE `test`='$url' AND `program`='$program' ORDER BY `serialNo_blocked` DESC, serialNo ASC LIMIT $offset, $limit");"""
    content = content.replace(old_sort_desc, new_sort_desc, 1)  # Nur das zweite Vorkommen
    print("✓ Sort-Queries hinzugefügt")
    
    # 4. Füge Tabellen-Header für RoboForex hinzu (vor Del)
    old_header = """<th class="adm_ref <?=($_COOKIE['showAdm']==1?'active':'');?>">Referral</th>
	<th>Del</th>"""
    new_header = """<th class="adm_ref <?=($_COOKIE['showAdm']==1?'active':'');?>">Referral</th>
	<th>RoboForex</th>
	<th>Del</th>"""
    content = content.replace(old_header, new_header)
    print("✓ Tabellen-Header erweitert")
    
    # 5. Account-Anzeige mit accountLogin erweitern
    old_account = """echo '<td class="account"><span class="cacc">'.$res['account']."</span></td>";"""
    new_account = """// Account-Nummer mit accountLogin wenn vorhanden
		$account_display = $res['account'];
		if(isset($res['accountLogin']) && !empty($res['accountLogin'])) {
			$account_display = $res['accountLogin'];
		}
		echo '<td class="account"><span class="cacc">'.$account_display."</span></td>";"""
    content = content.replace(old_account, new_account)
    print("✓ Account-Anzeige erweitert")
    
    # 6. Füge RoboForex-Status-Spalte vor Delete-Button hinzu
    # Suche nach dem Referral-Block und füge danach die neue Spalte ein
    pattern = r"(if\(\$res\['registrar'\] == \$res\['ref'\].*?\n\t\t\})"
    replacement = r"""\1
		// NEUE SPALTE: RoboForex Partner Status
		$roboStatus = isset($res['roboaffiliate']) ? $res['roboaffiliate'] : 'no';
		if($roboStatus == 'yes' || $roboStatus == '1' || $roboStatus == 1) {
			echo '<td style="text-align:center;color:#00AA00;font-weight:bold;">✓</td>';
		} else {
			echo '<td style="text-align:center;color:#AA0000;">✗</td>';
		}"""
    content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    print("✓ RoboForex-Status-Spalte hinzugefügt")
    
    # 7. Auch für die Suchtabelle unten die gleichen Änderungen
    # Header in der Suchtabelle
    old_search_header = """<th class=\"adm_ref '.($_COOKIE['showAdm']==1?'active':'').'\">Referral</th>
	<th>Del</th>"""
    new_search_header = """<th class=\"adm_ref '.($_COOKIE['showAdm']==1?'active':'').'\">Referral</th>
	<th>RoboForex</th>
	<th>Del</th>"""
    content = content.replace(old_search_header, new_search_header)
    
    # Account in der Suchtabelle
    old_search_account = """$_SESSION['search'][$z-1].= '<td class="account"><span class="cacc">'.$res['account']."</span></td>";"""
    new_search_account = """// Account mit accountLogin
		$account_display = $res['account'];
		if(isset($res['accountLogin']) && !empty($res['accountLogin'])) {
			$account_display = $res['accountLogin'];
		}
		$_SESSION['search'][$z-1].= '<td class="account"><span class="cacc">'.$account_display."</span></td>";"""
    content = content.replace(old_search_account, new_search_account)
    
    # RoboForex Status in der Suchtabelle (vor dem Delete-Button)
    pattern_search = r"(\$_SESSION\['search'\]\[\$z-1\]\.= '<td class=\"adm_ref adm_ref_t wrap.*?</td>';\n\t\t\})"
    replacement_search = r"""\1
		// RoboForex Partner Status
		$roboStatus = isset($res['roboaffiliate']) ? $res['roboaffiliate'] : 'no';
		if($roboStatus == 'yes' || $roboStatus == '1' || $roboStatus == 1) {
			$_SESSION['search'][$z-1].= '<td style="text-align:center;color:#00AA00;font-weight:bold;">✓</td>';
		} else {
			$_SESSION['search'][$z-1].= '<td style="text-align:center;color:#AA0000;">✗</td>';
		}"""
    content = re.sub(pattern_search, replacement_search, content, flags=re.DOTALL)
    print("✓ Suchtabelle erweitert")
    
    # Speichere die modifizierte Datei
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✓ Modifizierte Datei gespeichert: {output_file}")
    return True

if __name__ == "__main__":
    print("=== Template Modifikation für RoboForex-Spalte ===\n")
    
    input_file = 's:\\mt5\\daxovernight\\template.inc.php'
    output_file = 's:\\mt5\\daxovernight\\template_inc_complete.php'
    
    try:
        if modify_template(input_file, output_file):
            print("\n✓ Erfolgreich modifiziert!")
            print(f"\nDie neue Datei '{output_file}' ist bereit zum Upload.")
            print("\nÄnderungen:")
            print("1. SQL SELECT erweitert um 'roboaffiliate'")
            print("2. Sort-Option 'RoboForex Partner' hinzugefügt")
            print("3. Sort-Queries für roboaffiliate implementiert")
            print("4. Tabellen-Header um 'RoboForex' erweitert")
            print("5. Account-Anzeige nutzt jetzt 'accountLogin' wenn vorhanden")
            print("6. RoboForex-Status wird als ✓ oder ✗ angezeigt")
            print("7. Alle Änderungen auch in der Suchtabelle")
    except Exception as e:
        print(f"✗ Fehler: {e}")
