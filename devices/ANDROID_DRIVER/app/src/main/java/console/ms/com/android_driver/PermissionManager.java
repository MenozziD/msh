package console.ms.com.android_driver;

import android.Manifest;
import android.app.Service;
import android.content.Context;
import android.content.pm.PackageManager;
import android.support.v4.app.ActivityCompat;
import android.support.v4.content.ContextCompat;

import org.xmlpull.v1.XmlPullParser;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.security.Permission;
import java.util.ArrayList;
import java.util.List;

import console.ms.com.android_driver.MainActivity;
import console.ms.com.android_driver.ManageXml;
import console.ms.com.android_driver.R;

import static android.content.Context.MODE_PRIVATE;

public class PermissionManager {

    private String[] PERMISSIONS;
    private boolean permissionsOK;
    public boolean getpermissionsOK () {return permissionsOK;}
    public int PERMISSION_ALL;


    public PermissionManager (){
        PERMISSION_ALL = 1;
        PERMISSIONS= new String[2];
        PERMISSIONS[0] = Manifest.permission.WRITE_EXTERNAL_STORAGE;
        PERMISSIONS[1] = Manifest.permission.CAMERA;
    }

    static void requestPermission(MainActivity activity , String permission, int requestCode)
    {
        ActivityCompat.requestPermissions( activity, new String[] { permission }, requestCode);
    }

    public static boolean hasPermissions(Context context, String... permissions) {

        boolean result=false;
        if (context != null && permissions != null) {
            result=true;
            for (String permission : permissions) {
                if (ActivityCompat.checkSelfPermission(context, permission) != PackageManager.PERMISSION_GRANTED) {
                    result=false;
                }
            }
        }
        return result;
    }

    // Function to check and request permission
    public void checkPermissions(Context c)
    {
        permissionsOK=hasPermissions(c, PERMISSIONS);
        if (!permissionsOK && c != null && c.getClass().getSimpleName().equals("MainActivity")) {
            MainActivity activity = (MainActivity) c;
            ActivityCompat.requestPermissions(activity, PERMISSIONS, PERMISSION_ALL);
        }
    }

}

