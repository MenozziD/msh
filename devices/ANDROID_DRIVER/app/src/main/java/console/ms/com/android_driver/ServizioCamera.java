package console.ms.com.android_driver;

import android.app.Service;
        import android.content.Intent;
        import android.hardware.Camera;
        import android.hardware.Camera.Size;
        import android.media.MediaRecorder;
        import android.os.Environment;
        import android.os.IBinder;
        import android.util.Log;
        import android.view.SurfaceHolder;
        import android.view.SurfaceView;
        import android.widget.Toast;

        import java.io.IOException;
        import java.util.List;

public class ServizioCamera extends Service {
    private static final String TAG = "ServizioCamera";
    private SurfaceView mSurfaceView;
    private SurfaceHolder mSurfaceHolder;
    private static Camera mServiceCamera;
    private boolean mRecordingStatus;
    private MediaRecorder mMediaRecorder;

    @Override
    public void onCreate() {
        mRecordingStatus = false;
        mServiceCamera = MainActivity.mCamera;
        mSurfaceView = MainActivity.mSurfaceView;
        mSurfaceHolder = MainActivity.mSurfaceHolder;

        super.onCreate();
    }

    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        super.onStartCommand(intent, flags, startId);

        if (mRecordingStatus == false)
            startRecording();

        return START_STICKY;
    }

    @Override
    public void onDestroy() {
        stopRecording();
        mRecordingStatus = false;

        super.onDestroy();
    }

    public boolean startRecording(){
        boolean result=false;
        try {
            Toast.makeText(getBaseContext(), "Recording Started", Toast.LENGTH_SHORT).show();
            if (mServiceCamera != null) {
                Camera.Parameters params = mServiceCamera.getParameters();
                mServiceCamera.setParameters(params);
                Camera.Parameters p = mServiceCamera.getParameters();

                final List<Size> listPreviewSize = p.getSupportedPreviewSizes();
                for (Size size : listPreviewSize) {
                    Log.i(TAG, String.format("Supported Preview Size (%d, %d)", size.width, size.height));
                }

                Size previewSize = listPreviewSize.get(0);
                p.setPreviewSize(previewSize.width, previewSize.height);
                mServiceCamera.setParameters(p);

                try {
                    mServiceCamera.setPreviewDisplay(mSurfaceHolder);
                    mServiceCamera.startPreview();
                } catch (Exception e) {
                    Log.e(TAG, e.getMessage());
                    e.printStackTrace();
                }

                mServiceCamera.unlock();

                mMediaRecorder = new MediaRecorder();
                mMediaRecorder.setCamera(mServiceCamera);
                mMediaRecorder.setAudioSource(MediaRecorder.AudioSource.MIC);
                mMediaRecorder.setVideoSource(MediaRecorder.VideoSource.CAMERA);
                mMediaRecorder.setOutputFormat(MediaRecorder.OutputFormat.THREE_GPP);
                mMediaRecorder.setAudioEncoder(MediaRecorder.AudioEncoder.AMR_NB);
                mMediaRecorder.setVideoEncoder(MediaRecorder.VideoEncoder.H264);
                mMediaRecorder.setOutputFile(Environment.getExternalStorageDirectory().getPath() + "/video.mp4");
                mMediaRecorder.setPreviewDisplay(mSurfaceHolder.getSurface());

                mMediaRecorder.prepare();
                mMediaRecorder.start();

                mRecordingStatus = true;

                result= true;
            }

        } catch (IllegalStateException e) {
            Log.d(TAG, e.getMessage());
            e.printStackTrace();
            result= false;

        } catch (IOException e) {
            Log.d(TAG, e.getMessage());
            e.printStackTrace();
            result= false;
        } finally {
            return result;
        }
    }

    public void stopRecording() {
        Toast.makeText(getBaseContext(), "Recording Stopped", Toast.LENGTH_SHORT).show();
        try {
            mServiceCamera.reconnect();

        } catch (IOException e) {
            e.printStackTrace();
        }

        mMediaRecorder.stop();
        mMediaRecorder.reset();

        mServiceCamera.stopPreview();
        mMediaRecorder.release();

        mServiceCamera.release();
        mServiceCamera = null;
    }
}