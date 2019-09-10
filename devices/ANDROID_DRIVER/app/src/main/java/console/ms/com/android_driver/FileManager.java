package console.ms.com.android_driver;

import android.content.Context;
import android.os.Environment;
import android.util.Log;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.text.SimpleDateFormat;
import java.util.Date;

import static android.provider.MediaStore.Files.FileColumns.MEDIA_TYPE_IMAGE;
import static android.provider.MediaStore.Files.FileColumns.MEDIA_TYPE_VIDEO;


public class FileManager {
    final static String fileName = "log_data.txt";
    final static String path = Environment.getExternalStorageDirectory().getAbsolutePath() ;
    final static String TAG = FileManager.class.getName();
    final static String Log_Info="Info";
    final static String Log_Error="Error";
    final static String main_dir_name="ADTW";
    final static String log_dir_name="log";
    final static String webui_dir_name="webui";
    final static String webui_file_name="index.html";
    final static String config_file_name="config.xml";
    public static String getAbsPath(){return path+ File.separator +main_dir_name; }
    public static String getAbsConfigPath(){return path+ File.separator +main_dir_name+ File.separator +config_file_name; }



    private static File getOutputMediaFile(int type){
        // To be safe, you should check that the SDCard is mounted
        // using Environment.getExternalStorageState() before doing this.

        File mediaStorageDir = new File(Environment.getExternalStoragePublicDirectory(
                Environment.DIRECTORY_PICTURES), "MyCameraApp");
        // This location works best if you want the created images to be shared
        // between applications and persist after your app has been uninstalled.

        // Create the storage directory if it does not exist
        if (! mediaStorageDir.exists()){
            if (! mediaStorageDir.mkdirs()){
                Log.d("MyCameraApp", "failed to create directory");
                return null;
            }
        }

        // Create a media file name
        String timeStamp = new SimpleDateFormat("yyyyMMdd_HHmmss").format(new Date());
        File mediaFile;
        if (type == MEDIA_TYPE_IMAGE){
            mediaFile = new File(mediaStorageDir.getPath() + File.separator +
                    "IMG_"+ timeStamp + ".jpg");
        } else if(type == MEDIA_TYPE_VIDEO) {
            mediaFile = new File(mediaStorageDir.getPath() + File.separator +
                    "VID_"+ timeStamp + ".mp4");
        } else {
            return null;
        }

        return mediaFile;
    }

    public static void Log (String mex, String type){
        String result;
        SimpleDateFormat sdf = new SimpleDateFormat("dd/MM/yyyy HH:mm:ss");
        SimpleDateFormat sdf_file = new SimpleDateFormat("_dd_MM_yyyy");

        try{
            File file = new File(path+
                    File.separator+main_dir_name+
                    File.separator+
                    log_dir_name+File.separator+
                    fileName.replace("_data",
                            sdf_file.format(new Date())));
            if (!file.exists())
                file.createNewFile();
            result=sdf.format(new Date())+" "+type+"\n"+mex;
            saveToFile(file,result);
        }catch (Exception e){
            e.printStackTrace();
        }
    }

    public static  String ReadFile(String path,String fileName ){
        String result = null;

        try {
            FileInputStream fileInputStream = new FileInputStream (new File(path + fileName));
            InputStreamReader inputStreamReader = new InputStreamReader(fileInputStream);
            BufferedReader bufferedReader = new BufferedReader(inputStreamReader);
            StringBuilder stringBuilder = new StringBuilder();

            while ( (result = bufferedReader.readLine()) != null )
            {
                stringBuilder.append(result + System.getProperty("line.separator"));
            }
            fileInputStream.close();
            result = stringBuilder.toString();

            bufferedReader.close();
        }
        catch(FileNotFoundException ex) {
            Log.d(TAG, ex.getMessage());
        }
        catch(IOException ex) {
            Log.d(TAG, ex.getMessage());
        }
        return result;
    }


    static boolean saveToFile( File file, String data){
        try {
            //new File(path).mkdir();

            FileOutputStream fileOutputStream = new FileOutputStream(file,true);
            fileOutputStream.write((data + System.getProperty("line.separator")).getBytes());

            return true;
        }  catch(FileNotFoundException ex) {
            Log.d(TAG, ex.getMessage());
        }  catch(IOException ex) {
            Log.d(TAG, ex.getMessage());
        }
        return  false;
    }

    public static String getFileSeparator (){return File.separator;}

    public static void makeAppDirectory(){
        try {
            makeDirectory(path + File.separator, main_dir_name);
            makeDirectory(path + File.separator+main_dir_name,log_dir_name);
            makeDirectory(path + File.separator+main_dir_name,webui_dir_name);
        }catch (Exception e)
        {
            e.printStackTrace();
        }
    }


    public static void makeDirectory(String path,String dirname)
    {
        //File folder = new File(Environment.getExternalStorageDirectory() + File.separator + "STWS");
        File folder = new File(path + File.separator + dirname);
        boolean success = true;
        if (!folder.exists()) {
            success = folder.mkdirs();
        }
        if (success) {
            // Do something on success
        } else {
            // Do something else on failure
        }
    }


    private void deleteRecursive(File fileOrDirectory) {

        if (fileOrDirectory.isDirectory())
            for (File child : fileOrDirectory.listFiles())
                deleteRecursive(child);

        fileOrDirectory.delete();

    }

}

