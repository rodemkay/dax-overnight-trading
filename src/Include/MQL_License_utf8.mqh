#define FALSE 0
#define HINTERNET int
#define BOOL int
#define INTERNET_PORT int
#define LPINTERNET_BUFFERS uint
#define DWORD uint
#define DWORD_PTR uint
#define LPDWORD uint&
#define LPVOID uchar& 
#define LPSTR string
#define LPCWSTR ushort&
#define LPCTSTR string&
#define LPTSTR string&

#import "shell32.dll"
  int ShellExecuteW(int hwnd,          // Хендл родительского окна
                    string Operation,  // Указатель на строку операции. Open, Print, Explore
                    string File,       // Указатель на строку с именем исполняемого файла
                    string Parameters, // Указатель на строку с параметрами
                    string Directory,  // Указатель на строку с именем папки
                    int ShowCmd);      // 0 = показать
#import
#import "kernel32.dll"
  DWORD GetLastError(uint);
  bool GetVolumeInformationW(const string root_path_name,string volume_name_buffer,uint volume_name_size,uint &volume_serial_number[],
                              #ifdef __MQL4__ uint #else long #endif maximum_component_length,uint file_system_flags,string file_system_name_buffer,uint file_system_name_size);
  uint GetSystemFirmwareTable(uint firmware_table_provider_signature,uint firmware_table_id,uchar firmware_table_buffer,uint buffer_size);
  uint GetSystemFirmwareTable(uint firmware_table_provider_signature,uint firmware_table_id,uchar &firmware_table_buffer[],uint buffer_size);
#import
#import "wininet.dll"
	DWORD InternetAttemptConnect(DWORD dwReserved);
	HINTERNET InternetOpenW(LPCTSTR lpszAgent, DWORD dwAccessType, LPCTSTR lpszProxyName, LPCTSTR lpszProxyBypass, DWORD dwFlags);
	HINTERNET InternetConnectW(HINTERNET hInternet, LPCTSTR lpszServerName, INTERNET_PORT nServerPort, LPCTSTR lpszUsername, LPCTSTR lpszPassword, DWORD dwService, DWORD dwFlags, DWORD_PTR dwContext);
	HINTERNET HttpOpenRequestW(HINTERNET hConnect, LPCTSTR lpszVerb, LPCTSTR lpszObjectName, LPCTSTR lpszVersion, LPCTSTR lpszReferer, #ifdef __MQL4__ uint #else long #endif /*LPCTSTR* */ lplpszAcceptTypes, uint/*DWORD*/ dwFlags, DWORD_PTR dwContext);
	BOOL HttpSendRequestW(HINTERNET hRequest, LPCTSTR lpszHeaders, DWORD dwHeadersLength, LPVOID lpOptional[], DWORD dwOptionalLength);
	BOOL HttpQueryInfoW(HINTERNET hRequest, DWORD dwInfoLevel, LPVOID lpvBuffer[], LPDWORD lpdwBufferLength, LPDWORD lpdwIndex);
	HINTERNET InternetOpenUrlW(HINTERNET hInternet, LPCTSTR lpszUrl, LPCTSTR lpszHeaders, DWORD dwHeadersLength, uint /*DWORD*/ dwFlags, DWORD_PTR dwContext);
	BOOL InternetReadFile(HINTERNET hFile, LPVOID lpBuffer[], DWORD dwNumberOfBytesToRead, LPDWORD lpdwNumberOfBytesRead);
	BOOL InternetCloseHandle(HINTERNET hInternet);
	BOOL InternetSetOptionW(HINTERNET hInternet, DWORD dwOption, LPDWORD lpBuffer, DWORD dwBufferLength);
	BOOL InternetQueryOptionW(HINTERNET hInternet, DWORD dwOption, LPDWORD lpBuffer, LPDWORD lpdwBufferLength);
 	BOOL InternetSetCookieW(LPCTSTR lpszUrl, LPCTSTR lpszCookieName, LPCTSTR lpszCookieData);
	BOOL InternetGetCookieW(LPCTSTR lpszUrl, LPCTSTR lpszCookieName, LPVOID lpszCookieData[], LPDWORD lpdwSize);
	HINTERNET InternetReadFile(int hFile, int& lpvBuffer[], int lNumBytesToRead, int& lNumberOfBytesRead[]);
	HINTERNET InternetReadFile(int hFile, LPVOID lpvBuffer[], int lNumBytesToRead, int& lNumberOfBytesRead[]);
#import

#define OPEN_TYPE_PRECONFIG		               0   // использовать конфигурацию по умолчанию
#define INTERNET_SERVICE_FTP						   1   // сервис Ftp
#define INTERNET_SERVICE_HTTP						   3	 // сервис Http 
#define HTTP_QUERY_CONTENT_LENGTH 			      5
#define INTERNET_DEFAULT_HTTP_PORT  			   80
#define INTERNET_DEFAULT_HTTPS_PORT 			   443

#define INTERNET_FLAG_PRAGMA_NOCACHE				0x00000100  // не кешировать страницу
#define INTERNET_FLAG_KEEP_CONNECTION				0x00400000  // не разрывать соединение
#define INTERNET_FLAG_NO_AUTH            			0x00040000
#define INTERNET_FLAG_SECURE            			0x00800000
#define INTERNET_FLAG_RELOAD							0x80000000  // получать страницу с сервера при обращении к ней
#define INTERNET_OPTION_SECURITY_FLAGS    	   31

#define ERROR_INTERNET_INVALID_CA					12045
#define INTERNET_FLAG_IGNORE_CERT_DATE_INVALID  0x00002000
#define INTERNET_FLAG_IGNORE_CERT_CN_INVALID    0x00001000
#define SECURITY_FLAG_IGNORE_CERT_CN_INVALID    INTERNET_FLAG_IGNORE_CERT_CN_INVALID
#define SECURITY_FLAG_IGNORE_CERT_DATE_INVALID  INTERNET_FLAG_IGNORE_CERT_DATE_INVALID
#define SECURITY_FLAG_IGNORE_UNKNOWN_CA         0x00000100
#define SECURITY_FLAG_IGNORE_WRONG_USAGE        0x00000200

//------------------------------------------------------------------ struct tagRequest
struct tagRequest {
	string stVerb;    // метод запроса GET/POST
	string stObject;  // путь к странице "/get.php?a=1"  или "/index.htm"
	string stHead;    // заголовок запроса, 
						   // "Content-Type: multipart/form-data; boundary=1BEF0A57BE110FD467A\r\n"
						   // или "Content-Type: application/x-www-form-urlencoded"
	string stData;    // дополнительная строка данных
	bool fromFile;    // если =true, то stData обозначает имя файла данных
	string stOut;     // поле для приема ответа
	bool toFile;      // если =true, то stOut обозначает имя файла для приема ответа
	void Init(string aVerb, string aObject, string aHead, string aData, bool from, string aOut, bool to);
};
//------------------------------------------------------------------ class MqlNet
void tagRequest::Init(string aVerb, string aObject, string aHead, string aData, bool from, string aOut, bool to) {
	stVerb=aVerb;     // метод запроса GET/POST
	stObject=aObject; // путь к странице "/get.php?a=1"  или "/index.htm"
	stHead=aHead;     // заголовок запроса, "Content-Type: application/x-www-form-urlencoded"
	stData=aData;     // дополнительная строка данных
	fromFile=from;    // если =true, то stData обозначает имя файла данных
	stOut=aOut;       // поле для приема ответа
	toFile=to;        // если =true, то stOut обозначает имя файла для приема ответа
}
//------------------------------------------------------------------ class MqlNet
class MqlNet {
private:
	string Host; // имен хоста
	int Port; // порт
	string User; // имя пользователя
	string Pass; // пароль пользователя
	int Service; // тип сервиса 
	// получаемые параметры
	int hSession; // дескриптор сессии
	int hConnect; // дескриптор соединения
public:
	MqlNet(); // конструктор класса
	~MqlNet(); // деструктор
	bool _Open(string aHost, int aPort, string aUser, string aPass, int aService); // создаем сессию и открываем соединение
	void _Close(); // закрываем сессию и соединение
	bool Request(tagRequest &req); // отправляем запрос
	bool OpenURL(string aURL, string &Out, bool toFile); // просто читаем страницу в файл или в переменную
	void ReadPage(int hRequest, string &Out, bool toFile); // читсаем страницу
	long GetContentSize(int hURL); //получения информации о размере скачиваемой  страницы
	int FileToArray(string FileName, uchar& data[]); // копируем файл в массив для отправки
};
//------------------------------------------------------------------ MqlNet
void MqlNet::MqlNet() {
	hSession=-1; hConnect=-1; Host=""; User=""; Pass=""; Service=-1; // обнуляем параметры
}
//------------------------------------------------------------------ ~MqlNet
void MqlNet::~MqlNet() {
	_Close(); // закрываем все дескрипторы 
}
//------------------------------------------------------------------ _Open
long _dll=0;
bool MqlNet::_Open(string aHost, int aPort, string aUser, string aPass, int aService) {
	if (aHost=="") { Print("-Host not specified"); return(false); }
	if(!TerminalInfoInteger(TERMINAL_DLLS_ALLOWED)) {
	 datetime _tl=TimeLocal();
	 if(_dll<_tl) {
	  if(TerminalInfoString(TERMINAL_LANGUAGE)=="Russian") {
		Alert(Symbol(),": - DLL import отключен в терминале: Сервис -> Настройки -> Советники\n- Разрешить импорт DLL в настройках");
     } else {
      Alert(Symbol(),": - DLL import is disabled in terminal: Tools -> Options -> Expert Advisors\n- Allow DLL imports in settings");
     }
     _dll=_tl+15;
    }
    return(false); // проверка разрешенни DLL в терминале
   }
	if (hSession>0 || hConnect>0) _Close(); // если сессия была опеределена, то закрываем 
	//*************** Print("+Open Inet..."); // сообщение про попытку открытия в журнал
	if (InternetAttemptConnect(0)!=0) { Print("-Err AttemptConnect"); return(false); } // если не удалось проверить имеющееся соединение с интернетом, то выходим
	string UserAgent="Mozilla"; string nill="";
	hSession=InternetOpenW(UserAgent, OPEN_TYPE_PRECONFIG, nill, nill, 0); // открываем сессию
	if (hSession<=0) { Print("-Err create Session"); _Close(); return(false); } // если не смогли открыть сессию, то выходим
	hConnect=InternetConnectW(hSession, aHost, aPort, aUser, aPass, aService, 0, 0); 
	if (hConnect<=0) { Print("-Err create Connect"); _Close(); return(false); }
	Host=aHost; Port=aPort; User=aUser; Pass=aPass; Service=aService;
	return(true); // иначе все проверки завершились успешно
}
//------------------------------------------------------------------ _Close
void MqlNet::_Close() {
	if (hSession>0) { InternetCloseHandle(hSession); hSession=-1; /*Print("+Close Session...");**********************/ }
	if (hConnect>0) { InternetCloseHandle(hConnect); hConnect=-1; /*Print("+Close Connect...");**********************/ }
}
//------------------------------------------------------------------ Request
bool MqlNet::Request(tagRequest &req) {
	if (req.toFile && req.stOut=="") { Print("-File not specified "); return(false); }
	uchar _data[]; int hRequest=0, hSend=0; 
	string Vers="HTTP/1.1"; string nill="";
	if (req.fromFile) { if (FileToArray(req.stData, _data)<0) { Print("-Err reading file "+req.stData); return(false); } }// прочитали файл в массив
	else StringToCharArray(req.stData, _data);

	if (hSession<=0 || hConnect<=0) { _Close(); if (!_Open(Host, Port, User, Pass, Service)) { Print("-Err Connect"); _Close(); return(false); } }
	// создаем дескриптор запроса
	uint _FL=(Port==80?(INTERNET_FLAG_KEEP_CONNECTION|INTERNET_FLAG_RELOAD|INTERNET_FLAG_PRAGMA_NOCACHE):
 (INTERNET_FLAG_SECURE|INTERNET_FLAG_KEEP_CONNECTION|INTERNET_FLAG_RELOAD|INTERNET_FLAG_PRAGMA_NOCACHE));
	hRequest=HttpOpenRequestW(hConnect, req.stVerb, req.stObject, Vers, nill, 0, _FL, 0); 
	 if (hRequest<=0) { Print("-Err OpenRequest"); InternetCloseHandle(hConnect); return(false); }
	// отправляем запрос
	int n=0;
	while (n<2) {
		n++;
		hSend=HttpSendRequestW(hRequest, req.stHead, StringLen(req.stHead), _data, ArraySize(_data)); // отправили файл
		if (hSend<=0) 
		{ 	
			uint err=0; err=kernel32::GetLastError(err); Print("-Err SendRequest= ", err); 
			if (err!=ERROR_INTERNET_INVALID_CA) {
				uint dwFlags;
				uint dwBuffLen = sizeof(dwFlags);
				InternetQueryOptionW(hRequest, INTERNET_OPTION_SECURITY_FLAGS, dwFlags, dwBuffLen);
				dwFlags |= SECURITY_FLAG_IGNORE_UNKNOWN_CA;
				int rez=InternetSetOptionW(hRequest, INTERNET_OPTION_SECURITY_FLAGS, dwFlags, sizeof (dwFlags));
				if (!rez) { Print("-Err InternetSetOptionW= ", GetLastError()); break; }
			}
			else break;
		} 
		else break;
	}
	if (hSend>0/*&&dml.mon<5*/) ReadPage(hRequest, req.stOut, req.toFile); // читаем страницу
	InternetCloseHandle(hRequest); InternetCloseHandle(hSend); // закрыли все хендлы
	if (hSend<=0) _Close();
	return(true);
}
//------------------------------------------------------------------ OpenURL
bool MqlNet::OpenURL(string aURL, string &Out, bool toFile) {
	string nill="";
	if (hSession<=0 || hConnect<=0) { _Close(); if (!_Open(Host, Port, User, Pass, Service)) { Print("-Err Connect"); _Close(); return(false); } }
	uint _FL=(Port==80?(INTERNET_FLAG_RELOAD|INTERNET_FLAG_PRAGMA_NOCACHE):
   (INTERNET_FLAG_SECURE|INTERNET_FLAG_RELOAD|INTERNET_FLAG_PRAGMA_NOCACHE));
	int hURL=InternetOpenUrlW(hSession, aURL, nill, 0, _FL, 0); 
	if(hURL<=0) { Print("-Err OpenUrl"); return(false); }
	ReadPage(hURL, Out, toFile); // читаем в Out
	InternetCloseHandle(hURL); // закрыли 
	return(true);
}
//------------------------------------------------------------------ ReadPage
void MqlNet::ReadPage(int hRequest, string &Out, bool toFile) {
	// читаем страницу 
	uchar ch[100]; string toStr=""; uint dwBytes; int h=-1;
	if (toFile) h=FileOpen(Out, FILE_ANSI|FILE_BIN|FILE_WRITE);
	while(InternetReadFile(hRequest, ch, 100, dwBytes)) 
	{
	  if (dwBytes<=0) break; toStr=toStr+CharArrayToString(ch, 0, dwBytes);
	  if (toFile) for (uint i=0; i<dwBytes; i++) FileWriteInteger(h, ch[i], CHAR_VALUE);
	}
	if (toFile) { FileFlush(h); FileClose(h); }
	else Out=toStr;
}
//------------------------------------------------------------------ GetContentSize
long MqlNet::GetContentSize(int hRequest) {
	uint len=2048, ind=0; uchar buf[2048];
	int Res=HttpQueryInfoW(hRequest, HTTP_QUERY_CONTENT_LENGTH, buf, len, ind);
	if (Res<=0) { Print("-Err QueryInfo"); return(-1); }

	string _s=CharArrayToString(buf, 0, len);
	if (StringLen(_s)<=0) return(0);
	return(StringToInteger(_s));
}
//----------------------------------------------------- FileToArray
int MqlNet::FileToArray(string aFileName, uchar& _data[]) {
	int h, i, size;	
	h=FileOpen(aFileName, FILE_ANSI|FILE_BIN|FILE_READ);	if (h<0) return(-1);
	FileSeek(h, 0, SEEK_SET);	
	size=(int)FileSize(h); ArrayResize(_data, (int)size); 
	for (i=0; i<size; i++) _data[i]=(uchar)FileReadInteger(h, CHAR_VALUE); 
	FileClose(h); return(size);
 }
 MqlNet INet; // экземпляр класса для работы
//-----------------------------------------------------
//-----------------------------------------------------
//-----------------------------------------------------
//-----------------------------------------------------
//-----------------------------------------------------
//----------------------------------------------------- Activated
int License=0;
int _check=0;
bool YesKey=false;
string Package="";
string _ansTime="";
bool _email=false;
//--
//------------------------------------------------- OnTick()
bool Activation() {
  if(MQLInfoInteger(MQL_TESTER)) {
   YesKey=true;
   Package="MAX";
   return(true);
  }
  if(aInf.accL!=(string)AccountInfoInteger(ACCOUNT_LOGIN) || aInf.accL<"1") {
   DataOnInit(idt._domen,idt._port,prog,idt._prog,idt._vers,idt._URLbuy,idt._URLupdate,idt._ref,(int)idt._perc,idt.txUp,idt._mg,idt._code);
   Print("DataOnInit: ",aInf.accL);
   return(false);
  } 
  if(TerminalInfoInteger(TERMINAL_CONNECTED) && GetAnswer() && License<=1 && Package=="") {
    lSetLabel(0,prog+"Warning_t",(lng?"Купить программу: ":"Buy program: ")+prog,clrRed,68,idt.txUp,CORNER_RIGHT_UPPER,8,"Arial",ANCHOR_RIGHT_UPPER,false,false,"\n");
    lButtonCreate(prog+"Warning_b",65,idt.txUp,60,15,CORNER_RIGHT_UPPER,(lng?"Купить":"Purchase"),"\n","Arial",8);// Создание кнопки для перехода на сайт
   return(false);
  }
  if(TerminalInfoInteger(TERMINAL_CONNECTED) && GetAnswer() && _email==false) {
   return(false);
  }
//--
 return(true);
 }

//----------------------------------------------------- Start
long _TL=0;
MqlDateTime dml;
bool GetAnswer() {
static int _lcnz=0;
TimeLocal(dml);
_TL=(dml.day_of_week==6||dml.day_of_week==0?TimeLocal():TimeCurrent());
  if(IsDelay() && SendServer()) {
     if(_lcnz!=License) {
       if(License<2) {
        ObjectsDeleteAll(0,prog+"Warning_");
        ChartRedraw();
       }
       _lcnz=License;
     }
     License=2;
     YesKey=true;
  }
  return(true);
 }
//----------------------------------------------------- SendServer
MqlDateTime dt0,dt1;
bool SendServer() {
 static int _v=0;
  string acpr=_GetProfitMG(idt._mg);
 string accB=DoubleToString(AccountInfoDouble(ACCOUNT_BALANCE),0);
 string accE=DoubleToString(AccountInfoDouble(ACCOUNT_EQUITY),0);
 TimeToStruct(iTime(_Symbol,PERIOD_MN1,0),dt0);
 TimeToStruct(iTime(_Symbol,PERIOD_MN1,1),dt1);
 string accH=GetProfit(PERIOD_D1,0)+"~"+GetProfit(PERIOD_W1,0)+"~"+(string)dt1.mon+":"+GetProfit(PERIOD_MN1,1)+"~"+(string)dt0.mon+":"+GetProfit(PERIOD_MN1,0);
  string salt=(string)rndr(1000,9999);
  string keys="h4yT!H3/dA3K9z"+salt+"trl/xdFgj#erPjm";//32 symbols
  string psalt=CryptEncodeA(salt,"jlY2E9rzw/qJOd1S#G!28/k10C3!Sku5");//32 symbols
  string rs1=aInf.accL+"|"+aInf.accN+"|"+aInf.accC+"|"+prog+"|"+aInf.acct+"|"+idt._vers+"|"+aInf.mt+"|"+idt._ref+"|"+idt._perc+"|"+accB+"|"+accE;
  // Affiliate-Status aus GlobalVariables ableiten
  string affiliateStatus = "AFFILIATE_NONE";
  if(GlobalVariableCheck("ROBOFOREX_QNYJ_PERMANENT") && GlobalVariableGet("ROBOFOREX_QNYJ_PERMANENT") == 1.0)
    affiliateStatus = "AFFILIATE_VERIFIED";
  else if(GlobalVariableCheck("AFFILIATE_STATUS") && GlobalVariableGet("AFFILIATE_STATUS") == 1.0)
    affiliateStatus = "AFFILIATE_VERIFIED";

  string rs2=acpr+"|"+aInf.accS+"|"+aInf.accCurr+"|"+aInf.accTA+"|"+idt._driveID+"|"+idt._UUID+"|"+idt._code+"~"+accH+"|"+(string)_check+"|"+aInf.accO+"|"+affiliateStatus; // letztes Feld = req21
  string strSend="r1="+psalt+"$"+CryptEncodeA(rs1,keys)+"$"+CryptEncodeA(rs2,keys);
 // открываем сессию
 tagRequest req; // инициализация параметров
 if(INet._Open(idt._domen,idt._port,"","",INTERNET_SERVICE_HTTP)) {
  string Head="Content-Type: application/x-www-form-urlencoded";
  req.Init("POST","metatrader",Head,strSend,false,"",false);
   if(INet.Request(req)) {
    string ansServ=CryptDecodeA(req.stOut,keys); // Print("=======",req.stOut);
    string ans[];
    int RQ=StringSplit(ansServ,'|',ans);   //   Print(ansServ);
    if(StringFind(req.stOut,"403 Forbidden",0)>-1) Print(">>>>>>",req.stOut);
    if(RQ==2 && StringFind(ans[0],"::",0)>-1) { // Server errors\\The program is not registered in the system
      lSetLabel(0,prog+"Warning_te",ans[0],clrRed,100,idt.txUp-15,CORNER_RIGHT_UPPER,8,"Arial",ANCHOR_RIGHT_UPPER,false,false,"\n");
      if(StringFind(ans[0],"503",0)>-1) Print(ans[0],":",ans[1]);
       else Print(ans[0]);
      License=1;
      Package="";
      YesKey=false;
      return(false);
    }
    if(RQ==6) {
     _v=0;
     _ansTime=ans[0];
     if(StringLen(_ansTime)==10) {
      Package=ans[1];
      string _ansTX=ans[2];
      // Check-Period vom Server (ans[4]) in GlobalVariable speichern
      if(StringLen(ans[4]) > 0) {
        double checkPeriod = StringToDouble(ans[4]); // In Stunden
        if(checkPeriod > 0) {
          GlobalVariableSet("LICENSE_CHECK_PERIOD", checkPeriod);
          Print("Server Check-Period: ", checkPeriod, " Stunden");
        }
      }
        if(_ansTX=="Registered") {
         lSetLabel(0,prog+"Warning_t",prog+(lng?": Зарегистрировано до ":": Registered before ")+_ansTime,clrDeepSkyBlue,30,idt.txUp,CORNER_RIGHT_UPPER,8,"Arial",ANCHOR_RIGHT_UPPER,false,false,"\n");
         Print(lng?"Зарегистрировано до: ":"Registered before: ",_ansTime);
         _check=0;
         return(true);
        }
        
        if(StringFind(_ansTX,"Email not registered",0)>-1) {
         lSetLabel(0,prog+"Warning_t",prog+(lng?": E-mail не зарегистрирован":": Email not registered"),clrMagenta,74,idt.txUp,CORNER_RIGHT_UPPER,8,"Arial",ANCHOR_RIGHT_UPPER,false,false,"\n");
         lButtonCreate(prog+"Warning_be",70,idt.txUp,65,15,CORNER_RIGHT_UPPER,lng?" Регистрация":"Registration","\n","Arial",8);
         Print(lng?": E-mail не зарегистрирован":": Email not registered");
         _check=0;
         return(true);
        }
        
        double _ltu=(StringToTime(_ansTime)+86400-_TL)/3600.0;
        if(_ltu<24) {
          if(_ltu<0) return(false);
          lSetLabel(0,prog+"Warning_t",prog+(lng?": Лицензия истекает: ":": License expires: ")+_ansTime,clrDarkOrange,72,idt.txUp,CORNER_RIGHT_UPPER,8,"Arial",ANCHOR_RIGHT_UPPER,false,false,"\n");
          lButtonCreate(prog+"Warning_b",70,idt.txUp,60,15,CORNER_RIGHT_UPPER,lng?"Продлить":"Extend","\n","Arial",8);
          Print(lng?"Срок действия лицензии истекает: ":"License expires: ",_ansTime);
          _email=true;
          _check=(int)ans[4];//idt._tcheck;
          return(true);
        }
        if(_ansTX!=idt._vers) {
         lSetLabel(0,prog+"Warning_t",prog+(lng?": Обновите версию до:":": Upgrade to the version:"),clrDeepSkyBlue,72,idt.txUp,CORNER_RIGHT_UPPER,8,"Arial",ANCHOR_RIGHT_UPPER,false,false,"\n");
         lButtonCreate(prog+"Warning_bu",70,idt.txUp,60,15,CORNER_RIGHT_UPPER,"<"+_ansTX+">","\n","Arial",8);
         Print(lng?"Обновите версию программы до: ":"Update the program version to: ",_ansTX);
         if(ans[3]!="") lSetLabel(0,prog+"Warning_c",ans[3],clrSeaGreen,10,idt.txUp+15,CORNER_RIGHT_UPPER,9,"Arial",ANCHOR_RIGHT_UPPER,true,false,"\n");
         _email=true;
         _check=(int)ans[4];//idt._tcheck;
         return(true);
        }
        Print(lng?"Срок действия лицензии истекает: ":"License expires: ",_ansTime);
        _email=true;
        _check=(int)ans[4];//idt._tcheck;
        // Check-Period in GlobalVariable speichern
        if(StringToDouble(ans[4]) > 0) {
          GlobalVariableSet("LICENSE_CHECK_PERIOD", StringToDouble(ans[4]));
        }
        return(true);
      }
    }
    if(RQ<2) { // Сервер недоступен
     _v++;
     if(_v>3) { //если N ошибок - деактивируем
      License=1;
      Package="";
      YesKey=false;
      lSetLabel(0,prog+"Warning_te","Error. Try later",clrRed,100,idt.txUp-15,CORNER_RIGHT_UPPER,8,"Arial",ANCHOR_RIGHT_UPPER,false,false,"\n");
     }
      if(StringFind(req.stOut,"::",0)>-1) Print(req.stOut);
       else if(StringFind(req.stOut,"HY000",0)==-1) Print("Error (",_v,") ",req.stOut);
     return(false);
    }
   } else { Print("-err Request"); return(false); }
  } else { Print("-err iNetOpen"); return(false); }
  return(false);
 }
//----------------------------------------------------- DataOnInit
bool lng;
string prog;
  struct dataInit {
    string _domen;
    int    _port;
    string _prog;
    string _vers;
    string _URLbuy;
    string _URLupdate;
    string _ref;
    string _perc;
    int     txUp;
    int    _mg;
    string _code;
    string _driveID;
    string _UUID;
  };
 dataInit idt;
  struct dataAcc {
    string accL;
    string accO;
    string accTA;
    string acct;
    string accC;
    string accS;
    string accCurr;
    string accN;
    string mt;
  };
  dataAcc aInf;
  
//-------------------------------------------------
bool DataOnInit(string _domen_,int _port_,string _program_,string _prog_,string _version_,string _URLbuy_,string _URLupdate_,string _ref_,int _perc_,int _tx_sh_,int _mg_,string _code_) {
  MQLSetInteger(MQL_CODEPAGE,CP_ACP);
  ZeroMemory(idt);
  idt._domen=_domen_;
  idt._port=_port_;
  idt._vers=_version_;
  idt._URLbuy=_URLbuy_;
  idt._URLupdate=_URLupdate_;
  idt._ref=_ref_;
  idt._perc=(string)_perc_;
  idt.txUp=_tx_sh_;
  idt._mg=_mg_;
  idt._code=_code_;
  idt._UUID=SMBIOS::Read();
  idt._driveID=SystemDriveSerialNumber();
  //
  ZeroMemory(aInf);
  aInf.accL=(string)AccountInfoInteger(ACCOUNT_LOGIN);
  aInf.accO=(string)AccountInfoInteger(ACCOUNT_LIMIT_ORDERS);
  aInf.accTA=(string)AccountInfoInteger(ACCOUNT_TRADE_ALLOWED);
  aInf.acct=(string)AccountInfoInteger(ACCOUNT_TRADE_MODE);
  aInf.accC=AccountInfoString(ACCOUNT_COMPANY);
  aInf.accS=AccountInfoString(ACCOUNT_SERVER);
  aInf.accCurr=AccountInfoString(ACCOUNT_CURRENCY);
  aInf.accN=AccountInfoString(ACCOUNT_NAME);
  aInf.mt=#ifdef __MQL4__ "4" #else "5" #endif;
  ResetLastError();
  MathSrand(GetTickCount());
  lng=TerminalInfoString(TERMINAL_LANGUAGE)=="Russian";
  string result[];
  StringSplit(_prog_,'.',result);
  if(ArraySize(result) > 0)
    prog=result[0];//MQLInfoString(MQL_PROGRAM_NAME);
  else
    prog=_prog_;
  idt._prog=prog;
// От переименования
  if(prog!=_program_) {
   Alert(Symbol(),lng?"= Программа "+prog+" переименована!\nОригинальное имя: "+_program_+#ifdef __MQL4__ ".ex4" #else ".ex5" #endif:
                       "= The program "+prog+" was renamed!\nOriginal name: "+_program_+#ifdef __MQL4__ ".ex4" #else ".ex5" #endif);
   ExpertRemove();
   return(true);
  }
  // Создание кнопки для перехода на сайт
  lButtonCreate(prog+"Site",10,8,11,9,CORNER_RIGHT_LOWER,"",lng?"Перейти на сайт":"Go to the site","Arial",8,clrBlack,clrDodgerBlue);
//--
  return(false);
}
//-------------------------------------------------
void DataOnDeinit(int reason=0) {
  ObjectsDeleteAll(0,prog+"Warning_");
  ObjectsDeleteAll(0,prog+"Site");
  ChartRedraw();
}
//-------------------------------------------------
void ChartEventA(const int _id_,const string _sparam_) {
  if(_id_==CHARTEVENT_OBJECT_CLICK && (StringFind(_sparam_,"Warning_b")>0 || StringFind(_sparam_,"Site")>0)) {
   //-- Открывает сайт для покупки продукта
    if(ObjectGetInteger(0,prog+"Warning_b",OBJPROP_STATE)) {
      ObjectSetInteger(0,prog+"Warning_b",OBJPROP_STATE,false);
      ShellExecuteW(0,"Open",idt._URLbuy,"","",1);
    }
   //-- Открывает сайт для скачивания/обновления продукта
    if(ObjectGetInteger(0,prog+"Warning_bu",OBJPROP_STATE)) {
      ObjectSetInteger(0,prog+"Warning_bu",OBJPROP_STATE,false);
      ShellExecuteW(0,"Open",idt._URLupdate,"","",1);
    }
   //-- Переход на сайт
    if(ObjectGetInteger(0,prog+"Site",OBJPROP_STATE)) {
      ObjectSetInteger(0,prog+"Site",OBJPROP_STATE,false);
      ShellExecuteW(0,"Open",idt._URLupdate,"","",1);
    }
   //-- Открывает сайт для регистрации E-mail
    if(ObjectGetInteger(0,prog+"Warning_be",OBJPROP_STATE)) {
      ObjectSetInteger(0,prog+"Warning_be",OBJPROP_STATE,false);
      ShellExecuteW(0,"Open","https://"+idt._domen+"/register.php?acc="+aInf.accL,"","",1);
    }
    ChartRedraw();
  }
  if(_id_==CHARTEVENT_OBJECT_CLICK && StringFind(_sparam_,"Warning_t")>0) {
    ObjectsDeleteAll(0,prog+"Warning_");
    ChartRedraw();
  }
}
//----------------------------------------------------- Проверка не чаще чем раз в N час (min:2)
bool IsDelay() {
 int _delay=_check==0?15:_check*3600+(rand()%299+1);
 string _ngv=HexToInteger(prog);
 // переключение таймфрейма
  if(License==0) {
    return(true);
  }
 // нет лицензии - обновим переменную
  if(License==1) {
   GlobalVariableSet(_ngv+"_g",NormalizeDouble((_TL-_delay-60)/590.0,2));
  }
 // есть лицензия - обновим переменную
  if(License==2) {
   GlobalVariableSet(_ngv+"_q",NormalizeDouble((_TL-_delay-60)/790.0,2));
  }
 // нет лицензии - запишем в переменную
  if(License==1) {
   if((GlobalVariableGet(_ngv+"_q")*790.0)+_delay<_TL) {
    GlobalVariableSet(_ngv+"_q",NormalizeDouble(_TL/790.0,2));
    return(true);
   }
   return(false);
  }
 // есть лицензия - запишем в переменную
  if((GlobalVariableGet(_ngv+"_g")*590.0)+_delay<_TL) {
    GlobalVariableSet(_ngv+"_g",NormalizeDouble(_TL/590.0,2));
   return(true);
  }
  return(false);
}
//+------------------------------------------------------------------------------------------------------------------
void lSetLabel(int nwin=0,string nm="Label",string tx="txt",color clr=clrRed,int xd=0,int yd=0,ENUM_BASE_CORNER cr=0,
              int _font_size=8,string font="Arial",ENUM_ANCHOR_POINT an=0,bool sel=false,bool back=false,string tooltip="") {
  if(ObjectFind(0, nm)<0) {
    ObjectCreate(0, nm, OBJ_LABEL, nwin, 0, 0);
    ObjectSetInteger(0, nm, OBJPROP_CORNER, cr);
    ObjectSetInteger(0, nm, OBJPROP_ANCHOR, an);
    ObjectSetString (0, nm, OBJPROP_FONT, font);
    ObjectSetInteger(0, nm, OBJPROP_FONTSIZE, _font_size);
    ObjectSetInteger(0, nm, OBJPROP_SELECTABLE, sel);
    ObjectSetInteger(0, nm, OBJPROP_SELECTED,false);
    ObjectSetString (0, nm, OBJPROP_TOOLTIP, tooltip);
    ObjectSetInteger(0, nm, OBJPROP_BACK, back);
    ObjectSetInteger(0, nm, OBJPROP_HIDDEN,false);
  }
   ObjectSetInteger(0, nm, OBJPROP_XDISTANCE, xd);
   ObjectSetInteger(0, nm, OBJPROP_YDISTANCE, yd);
   ObjectSetString (0, nm, OBJPROP_TEXT, tx);
   ObjectSetInteger(0, nm, OBJPROP_COLOR, clr);
   ChartRedraw();
}
//+------------------------------------------------------------------------------------------------------------------
void lButtonCreate(string name="Button", int _xx=0, int _yy=0, int _width=50, int _height=18,
                   ENUM_BASE_CORNER _corner=CORNER_LEFT_UPPER, string _text="Button", string _tooltip="Button",
                   string _font="Arial", int _font_size=10, color _clr=clrBlack, color _back_clr=C'236,233,216') {
  if(ObjectFind(0,name)<0) {
      ObjectCreate(0,name,OBJ_BUTTON,0,0,0);
      ObjectSetInteger(0,name,OBJPROP_SELECTABLE,false);
      ObjectSetInteger(0,name,OBJPROP_SELECTED,false);
      ObjectSetInteger(0,name,OBJPROP_CORNER,_corner);
      ObjectSetInteger(0,name,OBJPROP_COLOR,_clr);
      ObjectSetInteger(0,name,OBJPROP_BORDER_COLOR,clrGray);
      ObjectSetInteger(0,name,OBJPROP_BGCOLOR,_back_clr);
      ObjectSetInteger(0,name,OBJPROP_STATE,false);
      ObjectSetInteger(0,name,OBJPROP_XSIZE,_width);
      ObjectSetInteger(0,name,OBJPROP_YSIZE,_height);
      ObjectSetString(0,name,OBJPROP_FONT,_font);
      ObjectSetInteger(0,name,OBJPROP_FONTSIZE,_font_size);
      ObjectSetInteger(0,name,OBJPROP_BACK,false);
      ObjectSetInteger(0,name,OBJPROP_HIDDEN,false);
      ObjectSetInteger(0,name,OBJPROP_ZORDER,0);
      ObjectSetString(0,name,OBJPROP_TOOLTIP,_tooltip);
     }
      ObjectSetInteger(0,name,OBJPROP_XDISTANCE,_xx);
      ObjectSetInteger(0,name,OBJPROP_YDISTANCE,_yy);
      ObjectSetString(0,name,OBJPROP_TEXT,_text);
}
//------------------------------------------------------------------------------------------------------
string _GetProfitMG(long _mg_) {
   double _pr=0;
   #ifdef __MQL4__
   for(int i=OrdersHistoryTotal()-1; i>=0; i--) {
      if(OrderSelect(i, SELECT_BY_POS, MODE_HISTORY)) {
         if((_mg_<0 || OrderMagicNumber()==_mg_) && OrderType()<2)
            _pr+=OrderProfit()+OrderCommission()+OrderSwap();
   }}
   #else
      if(HistorySelect(0, INT_MAX)) {
         for(int i=HistoryDealsTotal()-1; i>=0; i--) {
            const ulong Ticket = HistoryDealGetTicket(i);
            if((HistoryDealGetInteger(Ticket, DEAL_TYPE) <= DEAL_TYPE_SELL) &&
                 (_mg_<0 || HistoryDealGetInteger(Ticket, DEAL_MAGIC) == _mg_))
               _pr+= HistoryDealGetDouble(Ticket, DEAL_PROFIT) +
                     HistoryDealGetDouble(Ticket, DEAL_SWAP) +
                     HistoryDealGetDouble(Ticket, DEAL_COMMISSION) +
                     HistoryDealGetDouble(Ticket, DEAL_FEE);
      }}
   #endif
  return(DoubleToString(_pr,0));
}
//------------------------------------------------------------------------------------------------------
string GetProfit(ENUM_TIMEFRAMES _p_,int _n_)
{
  double pr=0;
  #ifdef __MQL4__
  for(int i=OrdersHistoryTotal()-1; i>=0 && !IsStopped(); i--) {
    if(OrderSelect(i, SELECT_BY_POS, MODE_HISTORY)) {
      if(OrderType()<2 && OrderMagicNumber()>0) {
        datetime OCT=OrderCloseTime();
        if(_n_==0)
         if(iTime(_Symbol,_p_,_n_)<OCT)
            pr+=OrderProfit()+OrderCommission()+OrderSwap();
        if(_n_>0) if(iTime(_Symbol,_p_,_n_)<OCT && iTime(_Symbol,_p_,_n_-1)>OCT)
            pr+=OrderProfit()+OrderCommission()+OrderSwap();
      }
    }
  }
   #else
      if(HistorySelect(0, INT_MAX)) {
         for(int i=HistoryDealsTotal()-1; i>=0; i--) {
            const ulong Ticket = HistoryDealGetTicket(i);
            if((HistoryDealGetInteger(Ticket, DEAL_TYPE) <= DEAL_TYPE_SELL) &&
                 (HistoryDealGetInteger(Ticket, DEAL_MAGIC) >0)) {
        datetime OCT=(datetime)HistoryDealGetInteger(Ticket, DEAL_TIME);
        if(_n_==0)
         if(iTime(_Symbol,_p_,_n_)<OCT)
            pr+=HistoryDealGetDouble(Ticket, DEAL_PROFIT) +HistoryDealGetDouble(Ticket, DEAL_SWAP) +HistoryDealGetDouble(Ticket, DEAL_COMMISSION) +HistoryDealGetDouble(Ticket, DEAL_FEE);
        if(_n_>0) if(iTime(_Symbol,_p_,_n_)<OCT && iTime(_Symbol,_p_,_n_-1)>OCT)
            pr+=HistoryDealGetDouble(Ticket, DEAL_PROFIT) +HistoryDealGetDouble(Ticket, DEAL_SWAP) +HistoryDealGetDouble(Ticket, DEAL_COMMISSION) +HistoryDealGetDouble(Ticket, DEAL_FEE);
      }}}
   #endif
  return(DoubleToString(pr,1));
}
//-------------------------------------------------------------------------------------------------------------------
string SystemDriveSerialNumber()
{
  uint iVolumeSerialNumber[1]= {0};
  string sVolumeSerialNumber="";
  if(GetVolumeInformationW("C:\\",NULL,15,iVolumeSerialNumber,0,0,NULL,15)) {
    sVolumeSerialNumber=IntegerToHexString(iVolumeSerialNumber[0]);
    sVolumeSerialNumber=StringSubstr(sVolumeSerialNumber,0,4)+"-"+StringSubstr(sVolumeSerialNumber,4);
  } else {
    sVolumeSerialNumber=GetID();
    sVolumeSerialNumber=StringSubstr(sVolumeSerialNumber,0,4)+"-"+StringSubstr(sVolumeSerialNumber,4);
  }
  return(sVolumeSerialNumber);
}
//-------------------------------------------------------------------------------------------------------------------
string GetID()
{
  string is="";
  if (!FileIsExist("mqlfile.dat",FILE_COMMON)) {
    int t1=(int)(TimeLocal());
    is=DecToHex(t1);
    int file_handle1=FileOpen("mqlfile.dat",FILE_READ|FILE_WRITE|FILE_BIN|FILE_COMMON);
    if (file_handle1!=INVALID_HANDLE) {
      FileWriteInteger(file_handle1,t1);
      FileClose(file_handle1);
    } else
      PrintFormat("Не удалось открыть файл. Код ошибки = %d",GetLastError());
  } else {
    int file_handle2=FileOpen("mqlfile.dat",FILE_READ|FILE_WRITE|FILE_BIN|FILE_COMMON);
    if (file_handle2!=INVALID_HANDLE) {
      int t2=FileReadInteger(file_handle2,INT_VALUE);
      is=DecToHex(t2);
      FileClose(file_handle2);
    }
  }
  return is;
}
//-----------------------------------------------
string DecToHex(int n)
{
  string s = "", c;
  while(n != 0) {
    if(n%16 < 10)
      c = CharToString((uchar)(n%16+'0'));
    else
      c = CharToString((uchar)(n%16+'A'-10));
    s = c + s;
    n = n / 16;
  }
  StringToLower(s);
  return s;
}
//-----------------------------------------------
string HexToInteger(string str) {
   int _result=0;
   for(int pos=StringLen(str)-1; pos>=0; pos--) {
      int c=StringGetCharacter(str,pos);
      int value = 0; 
      if(c>='0' && c<='9') value=c-'0';
      else if(c>='a' && c<='f') value=c-'a'+10;   
      else if(c>='A' && c<='F') value=c-'A'+10;
      else if(c>='A') value=c-'A'+10;
      _result+=value*17;
   }   
  return((string)_result);
}
//-----------------------------------------------
string IntegerToHexString(uint num) {
   char __hex[]= {'0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F'};
   int len=0,k=0;
   char buff[64];
   do {
      uint n=num&0xF;
      buff[len] = __hex[n];
      len++;
      num>>=4;
   } while(num!=0);
   for(; k<len/2; k++) {
      buff[k]^=buff[len-k-1];
      buff[len-k-1]^=buff[k];
      buff[k]^=buff[len-k-1];
   }
  return CharArrayToString(buff,0,len);
}
//------------------------------------------------------------------------------------------------------
union UUID16 {
   uchar b[16];
};
class SMBIOS
{
private:
   static UUID16     uuid;

public:
   static string     Read();
};
static UUID16  SMBIOS::uuid;
//--
static string SMBIOS::Read() {
   const uint SMBIOS_signature = ('R' << 24) + ('S' << 16) + ('M' << 8) + 'B';
   uint size = GetSystemFirmwareTable(SMBIOS_signature, 0, NULL, 0);
   uchar _data[];
   if(ArrayResize(_data, size) <= 0)
      return NULL;
   uint written = GetSystemFirmwareTable(SMBIOS_signature, 0, _data, size);
   if(written != size)
      return NULL;
   uint idx = 0;
   idx += 8;
   string sUUID=NULL;
   while(idx < size) {
      uchar type = _data[idx];
      uchar len = _data[idx + 1];
      if(len < 4)
         break;
      if(type == 1 && len >= 25) {
         idx += 8;
         bool all_zero = true, all_one = true;
         for(int i = 0; i < 16 && (all_zero || all_one); i++) {
            if(_data[idx + i] != 0x00)
               all_zero = false;
            if(_data[idx + i] != 0xFF)
               all_one = false;
         }
         if(!all_zero && !all_one) {
            uint idx2 = 0;
            sUUID += StringFormat("%02x", uuid.b[idx2++] = _data[idx + 3]);
            sUUID += StringFormat("%02x", uuid.b[idx2++] = _data[idx + 2]);
            sUUID += StringFormat("%02x", uuid.b[idx2++] = _data[idx + 1]);
            sUUID += StringFormat("%02x", uuid.b[idx2++] = _data[idx + 0]);
            sUUID += "-";
            sUUID += StringFormat("%02x", uuid.b[idx2++] = _data[idx + 5]);
            sUUID += StringFormat("%02x", uuid.b[idx2++] = _data[idx + 4]);
            sUUID += "-";
            sUUID += StringFormat("%02x", uuid.b[idx2++] = _data[idx + 7]);
            sUUID += StringFormat("%02x", uuid.b[idx2++] = _data[idx + 6]);
            sUUID += "-";
            for(int r = 8; r < 10; r++)
               sUUID += StringFormat("%02x", uuid.b[idx2++] = _data[idx + r]);
            sUUID += "-";
            for(int _w = 10; _w < 16; _w++)
               sUUID += StringFormat("%02x", uuid.b[idx2++] = _data[idx + _w]);
         }
         return sUUID;
      } else
         idx += len;
      do {
         int k = 0;
         while(idx + k < size && _data[idx + k] != 0)
            ++k;
         idx += k + 1;
      } while(_data[idx] != 0);
      ++idx;
   }
   return sUUID;
}
//------------------------------------------------------------------------------------------------------
string CryptEncodeA(string InputText,string key) {
   uchar scr[];
   uchar dst[];
   uchar res[];
   uchar key_aes256[];
   uchar key_base64[];
   StringToCharArray(InputText,scr);
   StringToCharArray(key,key_aes256);
   CryptEncode(CRYPT_AES256,scr,key_aes256,dst);
   CryptEncode(CRYPT_BASE64,dst,key_base64,res);
  return(CharArrayToString(res));
}
//--
string CryptDecodeA(string InputText,string key) {
   uchar scr[];
   uchar dst[];
   uchar res[];
   uchar key_base64[];
   uchar key_aes256[];
   StringToCharArray(InputText,scr,0,StringLen(InputText));
   StringToCharArray(key,key_aes256);
   CryptDecode(CRYPT_BASE64,scr,key_base64,dst);
   CryptDecode(CRYPT_AES256,dst,key_aes256,res);
  return(ArrayToString(res,true));
}
//------------------------------------------------------------------------------------------------------
int rndr(int mn,int mx,bool inclusive=true) {
   return(mn+rndn(mx-mn+(int)inclusive));
}
int rndn(int n) {
   if(n>32768 || n<0) return(-1);
   int r;
   while((r=MathRand())<32768%n);
   return(r%n);
}
//------------------------------------------------------------------------------------------------------
template<typename TChar>
string ArrayToString(const TChar &input_array[],bool remove_non_printable=false,int start=0,int count=-1,int codepage=CP_ACP) {
  struct cvt {
    static string convert(const uchar &input_array[],int start=0,int count=-1,int codepage=CP_ACP) {
      return(CharArrayToString(input_array,start,count,codepage));
    }
    static string convert(const short &input_array[],int start=0,int count=-1,int codepage=CP_ACP) {
      return(ShortArrayToString(input_array,start,count));
    }
  };
  int input_size =ArraySize(input_array);
  if(start>=input_size || count==0)
    return(NULL);
  if(start<0)
    start=0;
  if(count<0 || count==WHOLE_ARRAY || (start+count)>input_size)
    count=input_size-start;
  if(!remove_non_printable)
    return(cvt::convert(input_array,start,count,codepage));
  TChar cvt_array[];
  int   cvt_size=0;
  if(!ArrayResize(cvt_array,input_size))
    return(NULL);
  for(int i=0,n=start; i<input_size; i++) {
    const TChar input_sym = input_array[n++];
    if(input_sym>0 && input_sym<' ')
      continue;
    if(input_sym==0)
      break;
    cvt_array[cvt_size++]=input_sym;
  }
  return(cvt::convert(cvt_array,0,cvt_size));
}
//------------------------------------------------------------------------------------------------------