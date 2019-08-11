package console.ms.com.android_driver;

import android.hardware.Sensor;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
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
    ServizioADTW servizioADTW;
    ServerSocket httpServerSocket;
    static final int HttpServerPORT = 8888;
    static String msgLog = "";
    private API api;


    public WebServer(ServizioADTW pService) {
        servizioADTW = pService;
        webHttpServerThread = new HttpServerThread();
    }

    public HttpServerThread getHttpServerThread() {
        return webHttpServerThread;
    }


    public void close() {

        webHttpServerThread=null;
        if (httpServerSocket != null) {
            try {
                httpServerSocket.close();
            } catch (IOException e) {
                e.printStackTrace();
                FileManager.Log(e.toString(),FileManager.Log_Error);
            }
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


        public HttpServerThread() {
        }

        @Override
        public void run() {
            Socket socket = null;
            HttpResponseThread httpResponseThread=null;

            try {
                httpServerSocket = new ServerSocket(HttpServerPORT);

                while (true) {

                    socket = httpServerSocket.accept();
                    httpResponseThread =
                            new HttpResponseThread(
                                    socket);
                    httpResponseThread.start();
                }

            } catch (IOException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
                FileManager.Log(e.toString(),FileManager.Log_Error);
            }
        }
    }

    private class HttpResponseThread extends Thread {

        Socket socket;


        HttpResponseThread(Socket socket) {

            this.socket = socket;
        }


        @Override
        public void run() {
            BufferedReader is;
            PrintWriter os;
            String request;
            String[] arequest;
            API api;

            try {
                is = new BufferedReader(new InputStreamReader(socket.getInputStream()));
                request = is.readLine();

                os = new PrintWriter(socket.getOutputStream(), true);
                arequest = new String [3];
                arequest=request.split(" ");
                msgLog +="Method:".concat(arequest[0]+"\n");
                msgLog +="Resource:".concat(arequest[1]+"\n");
                msgLog +="HTTP Version:".concat(arequest[2]+"\n");
                os.print(servizioADTW.getAPI().route(arequest[1]));
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
