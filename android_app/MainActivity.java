package com.deepan.jarvis;

import android.content.Context;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.webkit.JavascriptInterface;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {
    private WebView webView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        webView = findViewById(R.id.webview);
        WebSettings webSettings = webView.getSettings();
        webSettings.setJavaScriptEnabled(true);
        webSettings.setDomStorageEnabled(true);
        webSettings.setAllowFileAccess(true);
        webSettings.setAllowContentAccess(true);
        
        // Add JavaScript Interface
        webView.addJavascriptInterface(new WebAppInterface(this), "Android");

        // Replace with your actual local IP or URL
        webView.setWebViewClient(new WebViewClient());
        webView.loadUrl("http://10.3.141.119:5000"); // Change this to your PC IP!
    }

    /**
     * Interface to expose Android methods to JavaScript.
     */
    public class WebAppInterface {
        Context mContext;

        WebAppInterface(Context c) {
            mContext = c;
        }

        @JavascriptInterface
        public void launchUrl(String url) {
            Intent intent = new Intent(Intent.ACTION_VIEW, Uri.parse(url));
            mContext.startActivity(intent);
        }

        @JavascriptInterface
        public void playYoutube(String query) {
            Intent intent = new Intent(Intent.ACTION_SEARCH);
            intent.setPackage("com.google.android.youtube");
            intent.putExtra("query", query);
            intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
            try {
                mContext.startActivity(intent);
            } catch (Exception e) {
                // Fallback to browser search if YouTube app is missing
                launchUrl("https://www.youtube.com/results?search_query=" + query);
            }
        }

        @JavascriptInterface
        public void launchApp(String appName) {
            // Simple toast for feedback
            Toast.makeText(mContext, "Opening " + appName + "...", Toast.LENGTH_SHORT).show();
            
            // Try to open popular apps by URI/Package if known
            String lowerName = appName.toLowerCase();
            if (lowerName.contains("spotify")) launchUrl("spotify:");
            else if (lowerName.contains("youtube")) launchUrl("vnd.youtube:");
            else if (lowerName.contains("chrome")) launchUrl("googlechrome://");
            else if (lowerName.contains("instagram")) launchUrl("instagram://");
            else {
                // Generic search or just inform user
                Toast.makeText(mContext, "Application deep link not found for: " + appName, Toast.LENGTH_LONG).show();
            }
        }
    }

    @Override
    public void onBackPressed() {
        if (webView.canGoBack()) {
            webView.setWebViewClient(new WebViewClient());
            webView.goBack();
        } else {
            super.onBackPressed();
        }
    }
}
