package console.ms.com.android_driver;

import android.hardware.Sensor;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.InetAddress;
import java.net.NetworkInterface;
import java.net.ServerSocket;
import java.net.Socket;
import java.net.SocketException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Enumeration;

public class WebServer   {

    private HttpServerThread webHttpServerThread;
    private API api;
    private ServizioADTW servizioADTW;
    private ServerSocket httpServerSocket;
    static final int HttpServerPORT = 8888;




    public WebServer(ServizioADTW pService) {
        servizioADTW = pService;
        api= new API(   servizioADTW.getSensorsOnBoard(),
                        servizioADTW.getResources().getString(R.string.html_index),
                        servizioADTW.getResources().getString(R.string.html_404),
                        servizioADTW.getManageXml()
                    );

        webHttpServerThread = new HttpServerThread();

    }

    public HttpServerThread getHttpServerThread() {
        return webHttpServerThread;
    }


    public void close() {

            try {
                if(webHttpServerThread!=null)
                    webHttpServerThread.cancel();

                httpServerSocket.close();
                webHttpServerThread=null;
                httpServerSocket=null;

            } catch (Exception e) {
                e.printStackTrace();
                FileManager.Log(e.toString(),FileManager.Log_Error);
            }

    }

    static String getIpAddress() {
        String ip = "127.0.0.1";
        try {
            Enumeration<NetworkInterface> enumNetworkInterfaces = NetworkInterface
                    .getNetworkInterfaces();
            while (enumNetworkInterfaces.hasMoreElements()) {
                NetworkInterface networkInterface = enumNetworkInterfaces
                        .nextElement();
                Enumeration<InetAddress> enumInetAddress = networkInterface
                        .getInetAddresses();
                while (enumInetAddress.hasMoreElements()) {
                    InetAddress inetAddress = enumInetAddress.nextElement();

                    if (inetAddress.isSiteLocalAddress()) {
                        ip = inetAddress.getHostAddress();
                    }
                }

            }

        } catch (SocketException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
            ip += "Something Wrong! " + e.toString() + "\n";
            FileManager.Log(e.toString(),FileManager.Log_Error);
        }

        return ip;
    }


    public class HttpServerThread extends Thread {


        private HttpResponseThread httpResponseThread=null;

        public HttpServerThread() {
        }

        @Override
        public void run() {
            try {
                Socket socket = null;
                    httpServerSocket = new ServerSocket(HttpServerPORT);
                    while (!Thread.currentThread().isInterrupted()) {
                        socket = httpServerSocket.accept();
                        httpResponseThread = new HttpResponseThread(socket, api);
                        httpResponseThread.start();
                    }
                } catch (IOException e1) {
                    e1.printStackTrace();
                }
        }

        public void cancel() { interrupt(); }



    }

    private class HttpResponseThread extends Thread {

        Socket socket;
        API api;


        HttpResponseThread(Socket socket,API api) {
            this.socket = socket;
            this.api=api;
        }


        @Override
        public void run() {
            BufferedReader is;
            PrintWriter os;
            String request;
            String[] arequest;
            API api;
            String msgLog = "";

            try {
                is = new BufferedReader(new InputStreamReader(socket.getInputStream()));
                request = is.readLine();

                os = new PrintWriter(socket.getOutputStream(), true);
                arequest = new String [3];
                arequest=request.split(" ");
                msgLog +="Method:".concat(arequest[0]+"\n");
                msgLog +="Resource:".concat(arequest[1]+"\n");
                msgLog +="HTTP Version:".concat(arequest[2]+"\n");
                os.print(this.api.route(arequest[1]));
                os.flush();
                socket.close();
                FileManager.Log(msgLog,FileManager.Log_Info);

            } catch (Exception e) {
                e.printStackTrace();
                FileManager.Log(e.toString(),FileManager.Log_Error);
            }

            return;
        }
    }


}
