package console.ms.com.android_driver;
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

    private MainActivity app;

    private LinearLayout.LayoutParams par_close;
    private LinearLayout.LayoutParams par_open;



    AscoltatoreMainActivity(MainActivity app){
        this.app=app;
        Display display = app.getWindowManager().getDefaultDisplay();
        Point size = new Point();
        display.getSize(size);

        par_close = new LinearLayout.LayoutParams(size.x,0,0);
        //par_open = new LinearLayout.LayoutParams(size.x,(size.y*20)/100,0);
        par_open = new LinearLayout.LayoutParams(size.x,LinearLayout.LayoutParams.WRAP_CONTENT,0);
    }

    @Override
    public void onClick(View v) {

        App this_app = App.getInstance();
        switch (v.getId()) {
            case R.id.bServer:
                if (app.getbServer().getTag().equals(app.getTAG_Server())) {
                    this_app.stopServerService();
                    app.gettvStatus().setText("OFF");
                    app.gettvStatus().setTextColor(Color.RED);
                    app.getbServer().setTag("");
                    app.getbServer().setBackgroundResource(R.drawable.play);
                }
                else {
                    this_app.startServerService();
                    app.getbServer().setTag(app.getTAG_Server());
                    app.gettvStatus().setText("ON");
                    app.gettvStatus().setTextColor(Color.GREEN);
                    app.getbServer().setBackgroundResource(R.drawable.stop);
                }
                break;

            /* SENSOR */
            case R.id.bSensorDim:
                if (app.getbSensorDim().getTag().equals(app.getTAG_Visible())) {
                    app.getVwSensor().setLayoutParams(par_close);
                    app.getVwSensor().setVisibility(View.INVISIBLE);
                    app.getbSensorDim().setTag("");
                    app.getbSensorDim().setBackgroundResource(R.drawable.left);
                }
                else {
                    app.getVwSensor().setVisibility(View.VISIBLE);
                    app.getVwSensor().setLayoutParams(par_open);
                    app.getbSensorDim().setTag(app.getTAG_Visible());
                    app.getbSensorDim().setBackgroundResource(R.drawable.down);
                    //Toast.makeText(app, "Start Scan...", Toast.LENGTH_SHORT).show();
                    //Toast.makeText(app, "Done", Toast.LENGTH_SHORT).show();
                }
                break;

            /* SET */
            case R.id.bSetDim:
                if (app.getbSetDim().getTag().equals(app.getTAG_Visible())) {
                    app.getVwSet().setLayoutParams(par_close);
                    app.getVwSet().setVisibility(View.INVISIBLE);
                    app.getbSetDim().setTag("");
                    app.getbSetDim().setBackgroundResource(R.drawable.left);
                }
                else {
                    app.getVwSet().setVisibility(View.VISIBLE);
                    app.getVwSet().setLayoutParams(par_open);
                    app.getbSetDim().setTag(app.getTAG_Visible());
                    app.getbSetDim().setBackgroundResource(R.drawable.down);
                    //Toast.makeText(app, "Start Scan...", Toast.LENGTH_SHORT).show();
                    //Toast.makeText(app, "Done", Toast.LENGTH_SHORT).show();
                }
                break;

            /* LOG */
            case R.id.bLogDim:
                if (app.getbLogDim().getTag().equals(app.getTAG_Visible())) {
                    app.getVwLog().setLayoutParams(par_close);
                    app.getVwLog().setVisibility(View.INVISIBLE);
                    app.getbLogDim().setTag("");
                    app.getbLogDim().setBackgroundResource(R.drawable.left);
                }
                else {

                    app.getVwLog().setVisibility(View.VISIBLE);
                    app.getVwLog().setLayoutParams(par_open);
                    app.getbLogDim().setTag(app.getTAG_Visible());
                    app.getbLogDim().setBackgroundResource(R.drawable.down);
                    //Toast.makeText(app, "Start Scan...", Toast.LENGTH_SHORT).show();
                    //Toast.makeText(app, "Done", Toast.LENGTH_SHORT).show();
                }
                break;
        }
    }
}
