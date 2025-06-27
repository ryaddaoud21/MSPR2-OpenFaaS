const gatewayUrl = "/f";  // Proxy Flask


// Authentification (login)
async function login() {
  const username = document.getElementById('li-username').value.trim();
  const password = document.getElementById('li-password').value.trim();
  const loginResult = document.getElementById('login-result');

  if (!username || !password) {
    loginResult.textContent = "⚠️ Veuillez remplir tous les champs.";
    return;
  }

  try {
    const res = await fetch(`${gatewayUrl}/authentication`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password }),
    });

    const data = await res.json();

    if (data.authenticated) {
      loginResult.textContent = "✅ Connexion réussie ! Redirection...";

      // Stocker username en sessionStorage
      sessionStorage.setItem('username', username);

      // Redirection après 1 seconde
      setTimeout(() => {
        window.location.href = 'dashboard.html';
      }, 1000);
    } else if (data.error) {
      loginResult.textContent = "❌ " + data.error;
    } else {
      loginResult.textContent = "❌ Identifiants invalides";
    }
  } catch (err) {
    loginResult.textContent = "❌ Erreur réseau ou serveur.";
  }
}

// Lier le formulaire login à la fonction login()
document.getElementById('login-form').addEventListener('submit', e => {
  e.preventDefault(); // Empêche le rechargement
  login();
});

async function signup() {
  const username = document.getElementById("su-username").value.trim();
  const password = document.getElementById("su-password").value.trim();

  if (!username || !password) {
    alert("Veuillez remplir tous les champs.");
    return;
  }

  const res = await fetch(`${gatewayUrl}/create-account-secure`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });

  const data = await res.json();
  document.getElementById("signup-result").textContent = JSON.stringify(data);

  // Ici on teste précisément si la création a réussi
  if (data.status === "✅ User created securely" || data.message === "✅ User created securely") {
    sessionStorage.setItem("username", username);
    setTimeout(() => {
      window.location.href = "dashboard.html";
    }, 1000);
  } else if (data.error) {
    alert("Erreur lors de la création du compte : " + data.error);
  }
}


// Générer secret TOTP + QR code (generate-2fa)
async function generate2FA() {
  const username = document.getElementById("v2fa-username").value.trim();

  if (!username) {
    alert("Veuillez saisir votre nom d'utilisateur.");
    return;
  }

  const res = await fetch(`${gatewayUrl}/generate-2fa`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username }),
  });

  const data = await res.json();

  if (data.qr_base64 || data.qrcode) {
    const qrCodeBase64 = data.qr_base64 || data.qrcode;
    document.getElementById("qr-image").src = `data:image/png;base64,${qrCodeBase64}`;
    document.getElementById("totp-secret").textContent = data.secret || "";
    document.getElementById("qr-section").style.display = "block";
  } else {
    alert(data.error || "Erreur lors de la génération du QR Code");
  }
}

// Vérifier code 2FA (verify-2fa)
async function verify2FA() {
  const username = document.getElementById("v2fa-username-verify").value.trim();
  const token = document.getElementById("v2fa-token").value.trim();

  if (!username || !token) {
    alert("Veuillez remplir tous les champs.");
    return;
  }

  const res = await fetch(`${gatewayUrl}/verify-2fa`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, token }),
  });

  const data = await res.json();

  if (data.message) {
    document.getElementById("verify-result").textContent = data.message;
  } else {
    document.getElementById("verify-result").textContent = data.error || "Code invalide";
  }
}

// Réinitialiser mot de passe (generate-password)
async function resetPassword() {
  const username = document.getElementById("rp-username").value.trim();

  if (!username) {
    alert("Veuillez saisir votre nom d'utilisateur.");
    return;
  }

  const res = await fetch(`${gatewayUrl}/generate-password`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username }),
  });

  const data = await res.json();

  if (data.password) {
    document.getElementById("reset-result").textContent = `Nouveau mot de passe : ${data.password}`;
  } else {
    document.getElementById("reset-result").textContent = data.error || "Erreur lors de la réinitialisation";
  }
}
