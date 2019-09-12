package console.ms.com.android_driver;
import android.Manifest;
import android.content.ClipData;
import android.content.ClipboardManager;
import android.content.Context;
import android.content.Intent;
import android.graphics.Color;
import android.graphics.Point;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.net.Uri;
import android.net.wifi.WifiManager;
import android.os.AsyncTask;
import android.os.Build;
import android.support.annotation.NonNull;
import android.support.annotation.Nullable;
import android.text.Html;
import android.text.TextUtils;
import android.util.Log;
import android.view.Display;
import android.view.View;
import android.widget.GridLayout;
import android.widget.LinearLayout;
import android.widget.Toast;


//import com.physicaloid.lib.usb.driver.uart.ReadLisener;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.Inet4Address;
import java.net.InetAddress;
import java.net.NetworkInterface;
import java.net.UnknownHostException;
import java.util.ArrayList;
import java.util.Enumeration;
import java.util.concurrent.ExecutionException;

public class AscoltatoreMainActivity  implements View.OnClickListener{

    private MainActivity activity;
    private App app;

    private LinearLayout.LayoutParams par_close;
    private LinearLayout.LayoutParams par_open;



    AscoltatoreMainActivity(MainActivity activity){
        app = App.getInstance();
        this.activity=activity;
        Display display = activity.getWindowManager().getDefaultDisplay();
        Point size = new Point();
        display.getSize(size);
        par_close = new LinearLayout.LayoutParams(size.x,0,0);
        //par_open = new LinearLayout.LayoutParams(size.x,(size.y*20)/100,0);
        par_open = new LinearLayout.LayoutParams(size.x,LinearLayout.LayoutParams.WRAP_CONTENT,0);
    }

    @Override
    public void onClick(View v) {
        try {
            switch (v.getId()) {
                case R.id.button_capture:
                    if (activity.IsOn) {
                        //mThread = new SocketClient(mPreview);
                        app.stopCameraService();
                        activity.IsOn = false;
                        activity.getButton().setText(R.string.stop);
                    } else {
                        Intent intent = new Intent(MainActivity.getActivity(), ServizioCamera.class);
                        intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
                        app.startCameraService();
                        activity.getButton().setText(R.string.start);
                        activity.IsOn = true;
                    }
                    break;

                case R.id.bServer:
                    if (activity.getbServer().getTag().equals(activity.getTAG_Server())) {
                        app.stopServerService();
                        activity.gettvStatus().setText("OFF");
                        activity.gettvStatus().setTextColor(Color.RED);
                        activity.getbServer().setTag("");
                        activity.getbServer().setBackgroundResource(R.drawable.play);
                        activity.gettvServer().setText("");
                    } else {
                        activity.getPermissionManager().checkPermissions(activity);
                        if (activity.getPermissionManager().getpermissionsOK()) {
                            app.startServerService();
                            activity.getbServer().setTag(activity.getTAG_Server());
                            activity.gettvStatus().setText("ON");
                            activity.gettvStatus().setTextColor(Color.GREEN);
                            activity.getbServer().setBackgroundResource(R.drawable.stop);
                            activity.gettvServer().setText(WebServer.getIpAddress() + ":" + WebServer.HttpServerPORT);
                        } else
                            Toast.makeText(app, activity.getResources().getString(R.string.mex_Alt), Toast.LENGTH_LONG).show();

                    }
                    break;
                case R.id.tvServer:
                    if (!activity.gettvServer().getText().toString().equals(""))
                        openWebPage(activity.gettvServer().getText().toString());
                    break;
                /* SENSOR */
                case R.id.bSensorDim:
                    if (activity.getbSensorDim().getTag().equals(activity.getTAG_Visible())) {
                        activity.getVwSensor().setLayoutParams(par_close);
                        activity.getVwSensor().setVisibility(View.INVISIBLE);
                        activity.getbSensorDim().setTag("");
                        activity.getbSensorDim().setBackgroundResource(R.drawable.left);
                    } else {
                        activity.getVwSensor().setVisibility(View.VISIBLE);
                        activity.getVwSensor().setLayoutParams(par_open);
                        activity.getbSensorDim().setTag(activity.getTAG_Visible());
                        activity.getbSensorDim().setBackgroundResource(R.drawable.down);
                        //Toast.makeText(app, "Start Scan...", Toast.LENGTH_SHORT).show();
                        //Toast.makeText(app, "Done", Toast.LENGTH_SHORT).show();
                    }
                    break;

                /* SET */
                case R.id.bSetDim:
                    if (activity.getbSetDim().getTag().equals(activity.getTAG_Visible())) {
                        activity.getVwSet().setLayoutParams(par_close);
                        activity.getVwSet().setVisibility(View.INVISIBLE);
                        activity.getbSetDim().setTag("");
                        activity.getbSetDim().setBackgroundResource(R.drawable.left);
                    } else {
                        activity.getVwSet().setVisibility(View.VISIBLE);
                        activity.getVwSet().setLayoutParams(par_open);
                        activity.getbSetDim().setTag(activity.getTAG_Visible());
                        activity.getbSetDim().setBackgroundResource(R.drawable.down);
                        //Toast.makeText(app, "Start Scan...", Toast.LENGTH_SHORT).show();
                        //Toast.makeText(app, "Done", Toast.LENGTH_SHORT).show();
                    }
                    break;

                /* LOG */
                case R.id.bLogDim:
                    if (activity.getbLogDim().getTag().equals(activity.getTAG_Visible())) {
                        activity.getVwLog().setLayoutParams(par_close);
                        activity.getVwLog().setVisibility(View.INVISIBLE);
                        activity.getbLogDim().setTag("");
                        activity.getbLogDim().setBackgroundResource(R.drawable.left);
                    } else {
                        activity.getVwLog().setVisibility(View.VISIBLE);
                        activity.getVwLog().setLayoutParams(par_open);
                        activity.getbLogDim().setTag(activity.getTAG_Visible());
                        activity.getbLogDim().setBackgroundResource(R.drawable.down);
                        if (activity.getPermissionManager().getpermissionsOK()) {
                            activity.gettvStatusLogMex().setText(activity.getResources().getString(R.string.mex_LOG_OK));
                            activity.gettvStatusLogMex().setTextColor(activity.getResources().getColor(R.color.colorGreen));
                        } else {
                            activity.gettvStatusLogMex().setText(activity.getResources().getString(R.string.mex_LOG_ERR));
                            activity.gettvStatusLogMex().setTextColor(activity.getResources().getColor(R.color.colorRed));
                        }
                        //Toast.makeText(app, "Start Scan...", Toast.LENGTH_SHORT).show();
                        //Toast.makeText(app, "Done", Toast.LENGTH_SHORT).show();
                    }
                    break;
                case R.id.bDeleteLog:

                    break;
            }
        } catch (Exception e) {
            e.printStackTrace();
            FileManager.Log(e.toString(),FileManager.Log_Error);
        }
    }

    private void openWebPage(String url) {
        if (!url.startsWith("http://") && !url.startsWith("https://"))
            url = "http://" + url;
        Intent intent = new Intent(Intent.ACTION_VIEW, Uri.parse(url));
        activity.startActivity(intent);
    }




}
