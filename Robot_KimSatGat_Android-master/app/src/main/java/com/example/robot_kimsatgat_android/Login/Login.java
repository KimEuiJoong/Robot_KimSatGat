package com.example.robot_kimsatgat_android.Login;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import com.example.robot_kimsatgat_android.R;
import com.google.android.gms.auth.api.signin.GoogleSignIn;
import com.google.android.gms.auth.api.signin.GoogleSignInAccount;
import com.google.android.gms.auth.api.signin.GoogleSignInClient;
import com.google.android.gms.auth.api.signin.GoogleSignInOptions;
import com.google.android.gms.common.SignInButton;
import com.google.android.gms.common.api.ApiException;
import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.Task;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class Login extends AppCompatActivity {
    GoogleSignInClient mGoogleSignInClient;
    ApiInterface api;

    int RC_SIGN_IN = 99;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.login);

        // Code for GoogleSignIn Starts
        // Configure sign-in to request the user's ID, email address, and basic
        // profile. ID and basic profile are included in DEFAULT_SIGN_IN.
        GoogleSignInOptions gso = new GoogleSignInOptions.Builder(GoogleSignInOptions.DEFAULT_SIGN_IN)
                .requestIdToken(getString(R.string.server_client_id))
                .requestEmail()
                .build();
        //if you need additional scope to access google apis, specify them with requestScopes
        // Build a GoogleSignInClient with the options specified by gso.
        //check if the user has already signed in to our app using google, on this device of another device



        mGoogleSignInClient = GoogleSignIn.getClient(this, gso);
        mGoogleSignInClient.silentSignIn()
                .addOnCompleteListener(
                        this,
                        new OnCompleteListener<GoogleSignInAccount>() {
                            @Override
                            public void onComplete(@NonNull Task<GoogleSignInAccount> task) {
                                handleSignInResult(task);
                            }
                        }
                );

        SignInButton signInButton = findViewById(R.id.sign_in_button);
        //signInButton.setSize(SignInButton.SIZE_STANDARD);
        signInButton.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View v){
                signIn();
            }
        });

        api = HttpClient.getRetrofit().create(ApiInterface.class);
        //Code for GoogleSignIn Ends


    }
    private void signIn(){
        Intent signInIntent = mGoogleSignInClient.getSignInIntent();
        startActivityForResult(signInIntent,RC_SIGN_IN);
    }

    private void signOut(){
        mGoogleSignInClient.signOut()
                .addOnCompleteListener(this, new OnCompleteListener<Void>() {
                    @Override
                    public void onComplete(@NonNull Task<Void> task) {
                        //
                    }
                });
    }
    private void revokeAccess(){
        mGoogleSignInClient.revokeAccess()
                .addOnCompleteListener(this, new OnCompleteListener<Void>() {
                    @Override
                    public void onComplete(@NonNull Task<Void> task) {
                        //
                    }
                });
    }

    @Override
    protected void onStart() {
        super.onStart();
        GoogleSignInAccount account = GoogleSignIn.getLastSignedInAccount(this);
        updateUI(account);
    }
    @Override
    public void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);

        // Result returned from launching the Intent from GoogleSignInClient.getSignInIntent(...);
        if (requestCode == RC_SIGN_IN) {
            // The Task returned from this call is always completed, no need to attach
            // a listener.
            Task<GoogleSignInAccount> task = GoogleSignIn.getSignedInAccountFromIntent(data);
            handleSignInResult(task);
        }
    }

    private void handleSignInResult(Task<GoogleSignInAccount> completedTask) {
        try {
            Log.w("msg","handlesignin");
            GoogleSignInAccount account = completedTask.getResult(ApiException.class);
            Log.w("msg","got account");
            String idToken = account.getIdToken();
            Log.w("msg","idToken:"+idToken);
            // Signed in successfully, show authenticated UI.
            //account.getEmail() : getGoogleEmail
            //account.getId() : getGoogleId
            //account.getIdToken() : getGoogleIdToken
            //getDisplayName,getGivenName,getFamilyName,getPhotoUrl,etc

            //send ID Token to server and validate
            //send ID Token with HTTPS REST

            ReqLoginData reqLoginData = new ReqLoginData(idToken);
            Call<ResLoginData> call = api.requestPostLogin(reqLoginData);

            call.enqueue(new Callback<ResLoginData>(){
                @Override
                public void onResponse(Call<ResLoginData> call, Response<ResLoginData> response){
                    Log.w("log", response.body().toString());
                }
                @Override
                public void onFailure(Call<ResLoginData> call, Throwable t){
                    Log.w("err","onFailure");
                }
            });


            //send ID Token to server ends
            updateUI(account);
        }catch (ApiException e) {
            // The ApiException status code indicates the detailed failure reason.
            // Please refer to the GoogleSignInStatusCodes class reference for more information.
            //Log.w("err", "signInResult:failed code=" + e.getStatusCode());
            Log.w("err", "signInResult:" + e.getMessage());
            updateUI(null);
        }
    }

    public void updateUI(GoogleSignInAccount account){
        if(account != null){
            Toast.makeText(this,"signed successfully",Toast.LENGTH_LONG).show();
        }else{
            Toast.makeText(this,"sign failed",Toast.LENGTH_LONG).show();
        }
    }
}