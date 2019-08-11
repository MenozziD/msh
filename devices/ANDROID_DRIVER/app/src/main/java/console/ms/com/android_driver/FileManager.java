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


public class FileManager {
    final static String fileName = "log_data.txt";
    final static String path = Environment.getExternalStorageDirectory().getAbsolutePath() ;
    final static String TAG = FileManager.class.getName();
    final static String Log_Info="Info";
    final static String Log_Error="Error";
    final static String main_dir_name="ADTW";
    final static String log_dir_name="log";



    public static void Log (String mex, String type){
        String result;
        SimpleDateFormat sdf = new SimpleDateFormat("dd/MM/yyyy HH:mm:ss");
        SimpleDateFormat sdf_file = new SimpleDateFormat("_dd_MM_yyyy");

        File file = new File(path+File.separator+main_dir_name+File.separator+log_dir_name+File.separator+fileName.replace("_data",sdf_file.format(new Date())));
        if (!file.exists()) {
            try {
                file.createNewFile();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
        result=sdf.format(new Date())+" "+type+"\n"+mex;
        saveToFile(file,result);
    }

    public static  String ReadFile( Context context){
        String line = null;

        try {
            FileInputStream fileInputStream = new FileInputStream (new File(path + fileName));
            InputStreamReader inputStreamReader = new InputStreamReader(fileInputStream);
            BufferedReader bufferedReader = new BufferedReader(inputStreamReader);
            StringBuilder stringBuilder = new StringBuilder();

            while ( (line = bufferedReader.readLine()) != null )
            {
                stringBuilder.append(line + System.getProperty("line.separator"));
            }
            fileInputStream.close();
            line = stringBuilder.toString();

            bufferedReader.close();
        }
        catch(FileNotFoundException ex) {
            Log.d(TAG, ex.getMessage());
        }
        catch(IOException ex) {
            Log.d(TAG, ex.getMessage());
        }
        return line;
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

