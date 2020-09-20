package console.ms.com.android_driver;


import android.net.Uri;

import java.io.ByteArrayInputStream;
import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.net.InetAddress;
import java.net.NetworkInterface;
import java.net.ServerSocket;
import java.net.Socket;
import java.net.SocketException;
import java.net.URI;
import java.net.URISyntaxException;
import java.net.URL;
import java.util.Arrays;
import java.util.Enumeration;

import org.apache.http.HttpEntity;
import org.apache.http.HttpException;
import org.apache.http.HttpRequest;
import org.apache.http.HttpResponse;
import org.apache.http.NameValuePair;
import org.apache.http.client.utils.URLEncodedUtils;
import org.apache.http.entity.ContentProducer;
import org.apache.http.entity.EntityTemplate;
import org.apache.http.impl.DefaultConnectionReuseStrategy;
import org.apache.http.impl.DefaultHttpResponseFactory;
import org.apache.http.impl.DefaultHttpServerConnection;
import org.apache.http.params.BasicHttpParams;
import org.apache.http.params.HttpParams;
import org.apache.http.params.HttpProtocolParams;
import org.apache.http.protocol.BasicHttpContext;
import org.apache.http.protocol.BasicHttpProcessor;
import org.apache.http.protocol.HTTP;
import org.apache.http.protocol.HttpContext;
import org.apache.http.protocol.HttpRequestHandler;
import org.apache.http.protocol.HttpRequestHandlerRegistry;
import org.apache.http.protocol.HttpService;
import org.apache.http.protocol.ResponseConnControl;
import org.apache.http.protocol.ResponseContent;
import org.apache.http.protocol.ResponseDate;
import org.apache.http.protocol.ResponseServer;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.List;

public class HttpServiceThread extends Thread {

    private String HTML_INDEX;
    private String HTML_404;
    ServerSocket serverSocket;
    Socket socket;
    HttpService httpService;
    BasicHttpContext basicHttpContext;
    static final int HttpServerPORT = 8888;
    boolean RUNNING = false;
    private ServizioADTW servizioADTW;

    HttpServiceThread(ServizioADTW servizioADTW, String HTML_INDEX,String HTML_404) {
        this.servizioADTW=servizioADTW;
        this.HTML_INDEX=HTML_INDEX;
        this.HTML_404=HTML_404;
        RUNNING = true;
        startHttpService();
    }

    @Override
    public void run() {

        try {
            serverSocket = new ServerSocket(HttpServerPORT);
            serverSocket.setReuseAddress(true);

            while (RUNNING) {
                socket = serverSocket.accept();
                DefaultHttpServerConnection httpServerConnection = new DefaultHttpServerConnection();
                HttpParams params = new BasicHttpParams();

                //params.setParameter(HttpProtocolParams.STRICT_TRANSFER_ENCODING,"chunked");

                httpServerConnection.bind(socket, params);
                httpService.handleRequest(httpServerConnection,basicHttpContext);

                //httpServerConnection.shutdown();
            }
            serverSocket.close();
        } catch (IOException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        } catch (HttpException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
    }

    private synchronized void startHttpService() {
        BasicHttpProcessor basicHttpProcessor = new BasicHttpProcessor();
        basicHttpContext = new BasicHttpContext();

        basicHttpProcessor.addInterceptor(new ResponseDate());
        basicHttpProcessor.addInterceptor(new ResponseServer());
        basicHttpProcessor.addInterceptor(new ResponseContent());
        basicHttpProcessor.addInterceptor(new ResponseConnControl());

        httpService = new HttpService(basicHttpProcessor,
                new DefaultConnectionReuseStrategy(),
                new DefaultHttpResponseFactory());

        HttpRequestHandlerRegistry registry = new HttpRequestHandlerRegistry();
        registry.register("/", new HomeCommandHandler());
        registry.register("/settings", new SettingsCommandHandler());
        registry.register("/sensor", new SensorCommandHandler());
        registry.register("/camera", new CameraCommandHandler());
        httpService.setHandlerResolver(registry);
    }

    public synchronized void stopServer() {
        RUNNING = false;
        if (serverSocket != null) {
            try {
                serverSocket.close();
            } catch (IOException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            }
        }
    }

    class HomeCommandHandler implements HttpRequestHandler {

        @Override
        public void handle(HttpRequest request, HttpResponse response,
                           HttpContext httpContext) throws HttpException, IOException {
            HttpEntity httpEntity = new EntityTemplate(
                    new ContentProducer() {

                        public void writeTo(final OutputStream outstream)
                                throws IOException {

                            OutputStreamWriter outputStreamWriter = new OutputStreamWriter(
                                    outstream, "UTF-8");
                            String path = FileManager.getAbsWebuiPath();
                            System.out.println("PATH: " + path);
                            //String resp=FileManager.ReadFile_Text(path,FileManager.webui_file_name);
                            String resp = "sdfasfd";
                            outputStreamWriter.write(resp);
                            System.out.println("RESPONSE: " + resp);
                            outputStreamWriter.flush();
                            outputStreamWriter.close();
                        }
                    });
            response.setHeader("Content-Type", "text/html");
            response.setEntity(httpEntity);
        }

    }

    class SettingsCommandHandler implements HttpRequestHandler {

        @Override
        public void handle(final HttpRequest request, HttpResponse response,
                           HttpContext httpContext) throws HttpException, IOException {

            HttpEntity httpEntity = new EntityTemplate(
                    new ContentProducer() {

                        public void writeTo(final OutputStream outstream)
                                throws IOException {

                            OutputStreamWriter outputStreamWriter = new OutputStreamWriter(
                                    outstream, "UTF-8");
                            String response = Settings(request);

                            outputStreamWriter.write(response);
                            outputStreamWriter.flush();
                            outputStreamWriter.close();
                        }
                    });
            response.setHeader("Content-Type", "application/json");
            response.setEntity(httpEntity);
        }

        public String Settings(HttpRequest request){


            NameValuePair listNameValuePair=null;
            NameValuePair cmdNameValuePair=null;
            NameValuePair settingNameValuePair=null;
            NameValuePair valueNameValuePair=null;

            List<NameValuePair> parameters = null;
            try {
                parameters = URLEncodedUtils.parse(new URI(
                        request.getRequestLine().getUri()), HTTP.UTF_8);
            } catch (URISyntaxException e) {
                e.printStackTrace();
            }

            for (NameValuePair nameValuePair : parameters) {
                if (nameValuePair.getName().equals("list"))
                    listNameValuePair=nameValuePair;

                if (nameValuePair.getName().equals("cmd"))
                    cmdNameValuePair=nameValuePair;

                if (nameValuePair.getName().equals("setting"))
                    settingNameValuePair=nameValuePair;

                if (nameValuePair.getName().equals("value"))
                    valueNameValuePair=nameValuePair;
                //System.out.println(nameValuePair.getName() + ": "+ nameValuePair.getValue());
            }

            String [] arraySettings= {"devicename","autoupdate","timeupdate"};
            String[] listCmd={"get","set"};
            String result=null;
            servizioADTW.getManageXml().readXml();
            JSONObject jsonObject=null;
            try {
                jsonObject = new JSONObject();
                if(settingNameValuePair!=null &&  Arrays.asList(listCmd).contains(cmdNameValuePair.getValue())) {
                    if (cmdNameValuePair.getValue().equals("set") && valueNameValuePair != null) {
                        servizioADTW.getManageXml().setFrontEndInfo(settingNameValuePair.getValue(), valueNameValuePair.getValue());
                        servizioADTW.getManageXml().writeXml();
                    }
                    jsonObject.put(settingNameValuePair.getValue(),servizioADTW.getManageXml().getFrontEndInfo(settingNameValuePair.getValue()));
                }
                if(listNameValuePair!=null ) {
                    if(listNameValuePair.getValue().equals("all") )
                    {
                        jsonObject.put("number",arraySettings.length);
                        jsonObject.put("settings", Arrays.toString(arraySettings));
                    }
                }
            } catch (JSONException e) {
                e.printStackTrace();
            } finally
            {
                result=jsonObject.toString();
                return result;
            }
        }


    }


    class SensorCommandHandler implements HttpRequestHandler {

        @Override
        public void handle(final HttpRequest request, HttpResponse response,
                           final HttpContext httpContext) throws HttpException, IOException {

            HttpEntity httpEntity = new EntityTemplate(
                    new ContentProducer() {

                        public void writeTo(final OutputStream outstream)
                                throws IOException {

                            OutputStreamWriter outputStreamWriter = new OutputStreamWriter(
                                    outstream, "UTF-8");

                            String response = Sensor(request);

                            outputStreamWriter.write(response);
                            outputStreamWriter.flush();
                            outputStreamWriter.close();
                        }
                    });
            response.setHeader("Content-Type", "application/json");
            response.setEntity(httpEntity);
        }

        public String Sensor(HttpRequest request){

            String result=null;

            NameValuePair listNameValuePair=null;
            NameValuePair typeNameValuePair=null;

            List<NameValuePair> parameters = null;
            try {
                parameters = URLEncodedUtils.parse(new URI(
                        request.getRequestLine().getUri()), HTTP.UTF_8);
            } catch (URISyntaxException e) {
                e.printStackTrace();
            }

            for (NameValuePair nameValuePair : parameters) {
                if (nameValuePair.getName().equals("list"))
                    listNameValuePair=nameValuePair;

                if (nameValuePair.getName().equals("type"))
                    typeNameValuePair=nameValuePair;

                //System.out.println(nameValuePair.getName() + ": "+ nameValuePair.getValue());
            }



            if(typeNameValuePair!=null) {
                if (servizioADTW.getSensorsOnBoard().getSensorByString(typeNameValuePair.getValue())!=null)
                    result = servizioADTW.getSensorsOnBoard().SensorToJSON(servizioADTW.getSensorsOnBoard().getSensorByString(typeNameValuePair.getValue())).toString();
                else
                    result="NOT INSTALL";
            }
            if(listNameValuePair!=null)
                result = servizioADTW.getSensorsOnBoard().SensorList(listNameValuePair.getValue()).toString();
            return result;
        }


    }

    class CameraCommandHandler implements HttpRequestHandler {

        @Override
        public void handle(final HttpRequest request, final HttpResponse response,
                           final HttpContext httpContext) throws HttpException, IOException {

            HttpEntity httpEntity = new EntityTemplate(
                    new ContentProducer() {

                        public void writeTo(final OutputStream outstream)
                                throws IOException {

                            outstream.write(Camera(request),0,Camera(request).length);

                            outstream.flush();
                            outstream.close();
                        }
                    });
            response.setHeader("Content-Type", "image/jpeg");
            //response.setHeader("Connection", "Keep-Alive");
            response.setEntity(httpEntity);
        }

        public byte[] Camera(HttpRequest request){

            byte[] result=null;

            NameValuePair listNameValuePair=null;
            NameValuePair typeNameValuePair=null;

            List<NameValuePair> parameters = null;
            try {
                parameters = URLEncodedUtils.parse(new URI(
                        request.getRequestLine().getUri()), HTTP.UTF_8);
            } catch (URISyntaxException e) {
                e.printStackTrace();
            }

            for (NameValuePair nameValuePair : parameters) {
                if (nameValuePair.getName().equals("list"))
                    listNameValuePair=nameValuePair;

                if (nameValuePair.getName().equals("type"))
                    typeNameValuePair=nameValuePair;

                //System.out.println(nameValuePair.getName() + ": "+ nameValuePair.getValue());
            }
            result=FileManager.ReadFile_Media(FileManager.getAbsStreamPath(),FileManager.stream_file_name);

            return result;
        }


    }

}
