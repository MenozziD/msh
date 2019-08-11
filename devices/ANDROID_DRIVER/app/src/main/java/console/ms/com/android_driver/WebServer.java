package console.ms.com.android_driver;

import android.app.PendingIntent;
import android.app.Service;
import android.content.Intent;
import android.hardware.Sensor;
import android.hardware.SensorManager;
import android.os.IBinder;
import android.support.annotation.Nullable;
import android.support.v4.app.NotificationCompat;
import android.widget.TextView;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.lang.reflect.InvocationTargetException;
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
    ServizioWebServer servizioWebServer;
    ServerSocket httpServerSocket;
    static final int HttpServerPORT = 8888;
    static String msgLog = "";



    public WebServer(ServizioWebServer pService) {
        servizioWebServer = pService;
        webHttpServerThread = new HttpServerThread();

    }

    public HttpServerThread getHttpServerThread() {
        return webHttpServerThread;
    }


    public void close() {
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

            try {
                httpServerSocket = new ServerSocket(HttpServerPORT);

                while (true) {
                    socket = httpServerSocket.accept();
                    HttpResponseThread httpResponseThread =
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

        public String route(String request) {
            String result = "";
            String content = "";
            String response = "";
            JSONObject jsonObject;
            SimpleDateFormat sdf = new SimpleDateFormat("dd/MM/yyyy HH:mm:ss");

            try {

                jsonObject = new JSONObject();
                jsonObject.put("request", request);
                jsonObject.put("response", "");
                jsonObject.put("timestamp", "");

                if (request.trim().equals("/")) {
                    response = servizioWebServer.getString(R.string.html_index);
                    response+= "\r\n";
                    content = "text/html";
                }

                if (request.indexOf("/sensor")>-1) {
                    String[] arr=request.split("\\?");
                    arr=arr[1].split("=");
                    if (arr[0].equals("type"))
                    {
                        if (arr[1].equals("LIGHT"))
                            jsonObject.put("response",servizioWebServer.getSensorsOnBoard().getListenerSensoreByType(Sensor.TYPE_LIGHT).getActualValue());
                        if (arr[1].equals("MAGNETIC_FIELD"))
                            jsonObject.put("response",servizioWebServer.getSensorsOnBoard().getListenerSensoreByType(Sensor.TYPE_MAGNETIC_FIELD).getActualValue());
                        if (arr[1].equals("PROXIMITY"))
                            jsonObject.put("response",servizioWebServer.getSensorsOnBoard().getListenerSensoreByType(Sensor.TYPE_PROXIMITY).getActualValue());
                    }
                    jsonObject.put("timestamp", sdf.format(new Date()));
                    response=jsonObject.toString();
                    content = "application/json";
                }
                if (request.indexOf("/settings")>-1) {
                    String[] arr=request.split("\\?");
                    arr=arr[1].split("=");
                    if (arr[0].equals("str_set")) {
                        if (arr[1].equals("time_update"))
                            jsonObject.put("response",servizioWebServer.getManageXml().get_timeupdate());
                        if (arr[1].equals("device_name"))
                            jsonObject.put("response", servizioWebServer.getManageXml().get_h1());
                    }
                    jsonObject.put("timestamp", sdf.format(new Date()));
                    response=jsonObject.toString();
                    content = "application/json";
                }
                if (content.equals(""))
                {
                    response = servizioWebServer.getString(R.string.html_404);
                    response+= "\r\n";
                    content = "text/html";
                }

            } catch (JSONException e) {
                response = e.toString();
                e.printStackTrace();
                FileManager.Log(e.toString(),FileManager.Log_Error);
            } catch (Exception e) {
                response = e.toString();
                e.printStackTrace();
                FileManager.Log(e.toString(),FileManager.Log_Error);
            } finally {

                result = "HTTP/1.0 200" + "\r\n";
                result += "Content type: " + content + "\r\n";
                result += "Content length: " + response.length() + "\r\n";
                result += "\r\n";
                result += response;

                return result;
            }
        }

        @Override
        public void run() {
            BufferedReader is;
            PrintWriter os;
            String request;
            String[] arequest;

            try {
                is = new BufferedReader(new InputStreamReader(socket.getInputStream()));
                request = is.readLine();

                os = new PrintWriter(socket.getOutputStream(), true);
                arequest = new String [3];
                arequest=request.split(" ");
                msgLog +="Method:".concat(arequest[0]+"\n");
                msgLog +="Resource:".concat(arequest[1]+"\n");
                msgLog +="HTTP Version:".concat(arequest[2]+"\n");

                os.print(route(arequest[1]));
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
