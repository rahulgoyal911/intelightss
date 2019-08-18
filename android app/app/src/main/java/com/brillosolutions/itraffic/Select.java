package com.brillosolutions.itraffic;

import android.annotation.SuppressLint;
import android.content.DialogInterface;
import android.os.Build;
import android.os.Handler;
import android.os.Message;
import androidx.core.app.ActivityCompat;
import android.support.v7.app.AlertDialog;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.content.Intent;
import android.widget.*;

import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;
import android.Manifest;
import android.content.pm.PackageManager;

import java.io.*;
import java.net.*;
public class Select extends AppCompatActivity implements LocationListener
{
    private String id, lat, lon;
    private Button sosButton;
    private String myLatitude, myLongitude;
    private LocationManager locationManager;
    private AlertDialog.Builder alertDialog;
    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_select);
        sosButton = (Button) findViewById(R.id.send_sos);
        sosButton.setEnabled(false);
        locationManager = (LocationManager)getSystemService(LOCATION_SERVICE);
        alertDialog = new AlertDialog.Builder(this);
        Bundle b = getIntent().getExtras();
        assert b != null;
        id = b.getString("id");
        lat = b.getString("lat");
        lon = b.getString("lon");
        askForPermission();
        Thread rxThread = new Thread(new Runnable()
        {
            @Override
            public void run()
            {
                try
                {
                    while (true)
                    {
                        String instanceLink = "http://intelights-api.anukai.com:8080/crossing/get_alert.php";
                        URL url = new URL(instanceLink);
                        URLConnection urlConnection = url.openConnection();
                        urlConnection.setDoOutput(true);
                        PrintStream postMan = new PrintStream(urlConnection.getOutputStream());
                        postMan.print("&id=" + id);
                        BufferedReader serverEcho = new BufferedReader
                                (new InputStreamReader(urlConnection.getInputStream()));
                        String msgLine, homeReply = "";
                        while ((msgLine = serverEcho.readLine()) != null)
                            homeReply += msgLine;
                        serverEcho.close();
                        Message rxdData = Message.obtain();
                        rxdData.obj = homeReply;
                        mHandler2.sendMessage(rxdData);
                        Thread.sleep(500);
                    }
                }
                catch (Exception ignored) {}
            }
        });rxThread.start();
    }

    public void btnClick(View v)
    {
        if(v.getId() == R.id.view_traffic)
        {
            Intent intent = new Intent(this, MapsActivity.class);
            intent.putExtra("id", id);
            intent.putExtra("lat", lat);
            intent.putExtra("lon", lon);
            startActivity(intent);
        }
        else
        {
            alertDialog.setTitle("Warning!")
                    .setMessage("Are you sure to send SoS message?")
                    .setPositiveButton("OK", new DialogInterface.OnClickListener()
                    {
                        @Override
                        public void onClick(DialogInterface dialog, int which)
                        {
                            Thread txThread = new Thread(new Runnable()
                            {
                                @Override
                                public void run()
                                {
                                    try
                                    {
                                        String instanceLink = "http://intelights-api.anukai.com:8080/crossing/sos_msg.php";
                                        URL url = new URL(instanceLink);
                                        URLConnection urlConnection = url.openConnection();
                                        urlConnection.setDoOutput(true);
                                        PrintStream postMan = new PrintStream(urlConnection.getOutputStream());
                                        postMan.print("&id=" + id);
                                        postMan.print("&msg=Accident occurred at intersection ID: " + id);
                                        postMan.print("&lat=" + myLatitude);
                                        postMan.print("&lon=" + myLongitude);
                                        BufferedReader serverEcho = new BufferedReader
                                                (new InputStreamReader(urlConnection.getInputStream()));
                                        String msgLine, homeReply = "";
                                        while ((msgLine = serverEcho.readLine()) != null)
                                            homeReply += msgLine;
                                        serverEcho.close();
                                        Message rxdData = Message.obtain();
                                        rxdData.obj = homeReply;
                                        mHandler.sendMessage(rxdData);
                                    }
                                    catch (final Exception ignored){}
                                }
                            });txThread.start();
                        }
                    })
                    .setNegativeButton("Cancel", new DialogInterface.OnClickListener()
                    {
                        @Override
                        public void onClick(DialogInterface dialog, int which) {}
                    }).show();
        }
    }
    @SuppressLint("HandlerLeak")
    Handler mHandler = new Handler()
    {
        private String rxdreply;
        @Override
        public void handleMessage(Message rxdMsg)
        {
            rxdreply = rxdMsg.obj.toString().trim();
            if (rxdreply.equals("1"))
                Toast.makeText(Select.this, "Your SoS request has been sent.", Toast.LENGTH_SHORT).show();
            else
                Toast.makeText(Select.this, "Server error!", Toast.LENGTH_SHORT).show();
        }
    };
    @SuppressLint("HandlerLeak")
    Handler mHandler2 = new Handler()
    {
        private String rxdreply, oldReply;
        @Override
        public void handleMessage(Message rxdMsg)
        {
            rxdreply = rxdMsg.obj.toString().trim();
            if (!rxdreply.equals(oldReply))
            {
                Toast.makeText(Select.this, rxdreply, Toast.LENGTH_SHORT).show();
                oldReply = rxdreply;
            }
        }
    };

    @Override
    public void onLocationChanged(Location location)
    {
        myLatitude = String.valueOf(location.getLatitude());
        myLongitude =  String.valueOf(location.getLongitude());
    }

    @Override
    public void onStatusChanged(String provider, int status, Bundle extras) {}

    @Override
    public void onProviderEnabled(String provider)
    {
        sosButton.setEnabled(true);
        Toast.makeText(Select.this, "Connected with GPS satellites.", Toast.LENGTH_SHORT).show();
    }

    @Override
    public void onProviderDisabled(String provider)
    {
        Toast.makeText(Select.this, "Enable GPS in your phone!", Toast.LENGTH_SHORT).show();
    }

    public void askForPermission()
    {
        if(ActivityCompat.checkSelfPermission
                (this, Manifest.permission.ACCESS_FINE_LOCATION)
                != PackageManager.PERMISSION_GRANTED
                && ActivityCompat.checkSelfPermission
                (this, Manifest.permission.ACCESS_COARSE_LOCATION)
                != PackageManager.PERMISSION_GRANTED)
        {
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M)
            {
                requestPermissions(new String[] {Manifest.permission.ACCESS_FINE_LOCATION,
                        Manifest.permission.ACCESS_COARSE_LOCATION}, 1);
            }
        }
        else
        {
            locationManager.requestLocationUpdates(LocationManager.GPS_PROVIDER, 1, 0, this);
            locationManager.requestLocationUpdates(LocationManager.NETWORK_PROVIDER, 1, 0, this);
        }
    }
}