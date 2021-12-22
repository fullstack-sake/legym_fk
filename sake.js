Java.perform(function(){
    var Log = Java.use("android.util.Log");
    
    Log.e("frida-HOOK",'')
	Log.e("frida-HOOK",'===')
	Log.e("frida-HOOK",'* Injecting hooks into common certificate pinning methods *')
	Log.e("frida-HOOK",'===')

	var X509TrustManager = Java.use('javax.net.ssl.X509TrustManager');
	var SSLContext = Java.use('javax.net.ssl.SSLContext');

	// build fake trust manager
	var TrustManager = Java.registerClass({
		name: 'com.sensepost.test.TrustManager',
		implements: [X509TrustManager],
		methods: {
			checkClientTrusted: function (chain, authType) {
			},
			checkServerTrusted: function (chain, authType) {
			},
			getAcceptedIssuers: function () {
				return [];
			}
		}
	});

	// pass our own custom trust manager through when requested
	var TrustManagers = [TrustManager.$new()];
	var SSLContext_init = SSLContext.init.overload(
		'[Ljavax.net.ssl.KeyManager;', '[Ljavax.net.ssl.TrustManager;', 'java.security.SecureRandom'
	);
	SSLContext_init.implementation = function (keyManager, trustManager, secureRandom) {
		Log.e("frida-HOOK",'! Intercepted trustmanager request');
		SSLContext_init.call(this, keyManager, TrustManagers, secureRandom);
	};

	Log.e("frida-HOOK",'* Setup custom trust manager');

	// okhttp3
	try {
		var CertificatePinner = Java.use('okhttp3.CertificatePinner');
		CertificatePinner.check.overload('java.lang.String', 'java.util.List').implementation = function (str) {
			Log.e("frida-HOOK",'! Intercepted okhttp3: ' + str);
			return;
		};

		Log.e("frida-HOOK",'* Setup okhttp3 pinning')
	} catch(err) {
		Log.e("frida-HOOK",'* Unable to hook into okhttp3 pinner')
	}

	// trustkit
	try {
		var Activity = Java.use("com.datatheorem.android.trustkit.pinning.OkHostnameVerifier");
		Activity.verify.overload('java.lang.String', 'javax.net.ssl.SSLSession').implementation = function (str) {
			Log.e("frida-HOOK",'! Intercepted trustkit{1}: ' + str);
			return true;
		};

		Activity.verify.overload('java.lang.String', 'java.security.cert.X509Certificate').implementation = function (str) {
			Log.e("frida-HOOK",'! Intercepted trustkit{2}: ' + str);
			return true;
		};

		Log.e("frida-HOOK",'* Setup trustkit pinning')
	} catch(err) {
		Log.e("frida-HOOK",'* Unable to hook into trustkit pinner')
	}

	// TrustManagerImpl
	try {
		var TrustManagerImpl = Java.use('com.android.org.conscrypt.TrustManagerImpl');
		TrustManagerImpl.verifyChain.implementation = function (untrustedChain, trustAnchorChain, host, clientAuth, ocspData, tlsSctData) {
			Log.e("frida-HOOK",'! Intercepted TrustManagerImp: ' + host);
			return untrustedChain;
		}

		Log.e("frida-HOOK",'* Setup TrustManagerImpl pinning')
	} catch (err) {
		Log.e("frida-HOOK",'* Unable to hook into TrustManagerImpl')
	}

	// Appcelerator
	try {
		var PinningTrustManager = Java.use('appcelerator.https.PinningTrustManager');
		PinningTrustManager.checkServerTrusted.implementation = function () {
			Log.e("frida-HOOK",'! Intercepted Appcelerator');
		}

		Log.e("frida-HOOK",'* Setup Appcelerator pinning')
	} catch (err) {
		Log.e("frida-HOOK",'* Unable to hook into Appcelerator pinning')
	}
	
	// ByPass SSL pinning for Android 7+
	var array_list = Java.use("java.util.ArrayList");
	var ApiClient = Java.use('com.android.org.conscrypt.TrustManagerImpl');
	ApiClient.checkTrustedRecursive.implementation = function(a1,a2,a3,a4,a5,a6) {
		Log.e("frida-HOOK",'Bypassing SSL Pinning');
		var k = array_list.$new();
		return k;
	}

	// Force mode debug for all webview
	var WebView = Java.use('android.webkit.WebView');
	WebView.loadUrl.overload("java.lang.String").implementation = function (s) {
		Log.e("frida-HOOK",'Enable webview debug for URL: '+s.toString());
		this.setWebContentsDebuggingEnabled(true);
		this.loadUrl.overload("java.lang.String").call(this, s);
	};
})



Java.perform(function() {
    var Log = Java.use("android.util.Log");
    Log.e("frida-HOOK", "Have fun!");
	
    Java.use("java.security.KeyStore$PrivateKeyEntry").getPrivateKey.implementation = function() {
        Log.e("frida-HOOK", "[java.security.KeyStore$PrivateKeyEntry.getPrivateKey] Called");
        var result = this.getPrivateKey();
		let filePath = "/sdcard/Download/client_keystore_" + "_" + getNowTime() + '.p12';
        dump2sdcard(this.getPrivateKey(), this.getCertificate(), filePath);
        return result;
    }
	
    Java.use("java.security.KeyStore$PrivateKeyEntry").getCertificateChain.implementation = function() {
        Log.e("frida-HOOK", "[java.security.KeyStore$PrivateKeyEntry.getCertificateChain] Called");
        var result = this.getCertificateChain();
		let filePath = "/sdcard/Download/client_keystore_" + "_" + getNowTime() + '.p12';
        dump2sdcard(this.getPrivateKey(), this.getCertificate(), filePath);
        return result;
    }
})


