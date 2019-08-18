package com.brillosolutions.itraffic;

import android.annotation.SuppressLint;
import android.os.Handler;
import android.os.Message;
import androidx.core.app.FragmentActivity;
import android.os.Bundle;
import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.OnMapReadyCallback;
import com.google.android.gms.maps.SupportMapFragment;
import com.google.android.gms.maps.model.BitmapDescriptorFactory;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.MarkerOptions;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.PrintStream;
import java.net.URL;
import java.net.URLConnection;
import java.util.Objects;

public class MapsActivity extends FragmentActivity implements OnMapReadyCallback
{

    private GoogleMap mMap;
    private double latitude, longitude;
    private String usrID, instanceLink;
    private URL url;
    private URLConnection urlConnection;
    private int j , k = 0;
    private double[] intSec1001 = {30.730719, 76.782085, 30.729446, 76.787857, 30.724780, 76.787492, 30.725536, 76.781570};
    private double[] intSec1002 = {30.737715, 76.793532, 30.736911, 76.799752, 30.731913, 76.798685, 30.732552, 76.792632};
    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_maps);
        SupportMapFragment mapFragment = (SupportMapFragment) getSupportFragmentManager()
                .findFragmentById(R.id.map);
        if (mapFragment != null) {
            mapFragment.getMapAsync(this);
        }
        Bundle b = getIntent().getExtras();
        assert b != null;
        latitude = Double.valueOf(Objects.requireNonNull(b.getString("lat")));
        longitude = Double.valueOf(Objects.requireNonNull(b.getString("lon")));
        usrID = b.getString("id");
        Thread rxThread = new Thread(new Runnable()
        {
            @Override
            public void run()
            {
                try
                {
                    while (true)
                    {
                        instanceLink = "http://intelights-api.anukai.com:8080/crossing/getLaneData.php";
                        url = new URL(instanceLink);
                        urlConnection = url.openConnection();
                        urlConnection.setDoOutput(true);
                        PrintStream postMan = new PrintStream(urlConnection.getOutputStream());
                        postMan.print("&id=" + usrID);
                        BufferedReader serverEcho = new BufferedReader
                                (new InputStreamReader(urlConnection.getInputStream()));
                        String msgLine, homeReply = "";
                        while ((msgLine = serverEcho.readLine()) != null)
                            homeReply += msgLine;
                        serverEcho.close();
                        Message rxdData = Message.obtain();
                        rxdData.obj = homeReply;
                        mHandler.sendMessage(rxdData);
                        Thread.sleep(300);
                    }
                }
                catch (Exception ignored) {}
            }
        });rxThread.start();
    }

    @Override
    public void onMapReady(GoogleMap googleMap)
    {
        mMap = googleMap;
        LatLng location = new LatLng(latitude, longitude);
        mMap.moveCamera(CameraUpdateFactory.newLatLng(location));
        placeMarkers();
    }

    public void placeMarkers()
    {
        if(usrID.equals("1001"))
        {
            for(int i = 0; i <= intSec1001.length - 1; i += 2)
            {
                mMap.addMarker(new MarkerOptions()
                        .icon(BitmapDescriptorFactory.defaultMarker(BitmapDescriptorFactory.HUE_RED))
                        .position(new LatLng(intSec1001[i], intSec1001[i + 1])));
            }
        }
        else
        {
            for(int i = 0; i <= intSec1002.length - 1; i += 2)
            {
                mMap.addMarker(new MarkerOptions()
                        .icon(BitmapDescriptorFactory.defaultMarker(BitmapDescriptorFactory.HUE_RED))
                        .position(new LatLng(intSec1002[i], intSec1002[i + 1])));
            }
        }
    }

    @SuppressLint("HandlerLeak")
    Handler mHandler = new Handler()
    {
        private String rxdReply;
        @Override
        public void handleMessage(Message rxdMsg)
        {
            rxdReply = rxdMsg.obj.toString().trim();
            String[] breakReply = rxdReply.split(",");
           if (usrID.equals("1001"))
               getGeoPoints(intSec1001, breakReply);
           else
               getGeoPoints(intSec1002, breakReply);
            super.handleMessage(rxdMsg);
        }

        void getGeoPoints(double[] geoPointsArray, String[] markerData)
        {
            if(k <= 3)
            {
                showOnMap(geoPointsArray[j], geoPointsArray[j + 1], "[LANE - 1]: " + markerData[k] + " VEHICLES", Integer.parseInt(markerData[4]));
                j += 2;
                k++;
                if (k > 3)
                    j = k = 0;
            }
        }

        void showOnMap(double lat, double lon, String info, int light)
        {
            if(k + 1 == light)
            {
                mMap.addMarker(new MarkerOptions()
                        .icon(BitmapDescriptorFactory.defaultMarker(BitmapDescriptorFactory.HUE_GREEN))
                        .position(new LatLng(lat, lon))
                        .title(info)).showInfoWindow();
            }
            else
            {
                mMap.addMarker(new MarkerOptions()
                        .icon(BitmapDescriptorFactory.defaultMarker(BitmapDescriptorFactory.HUE_RED))
                        .position(new LatLng(lat, lon))
                        .title(info)).showInfoWindow();
            }
        }
    };
}