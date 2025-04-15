const form = document.getElementById("input-form");
const functionButton = document.getElementById("function-btn");
const display = document.getElementById("display");

const url = "http://localhost:8000";
//animation class
const animation_class = "text-writer-animation";
const algorithm_selector = document.getElementById("algorithm-selector");
const decryptCheckbox = document.getElementById("decrypt");
const exportDataBtn = document.getElementById("exporter");
const Algorithms = Object.freeze({
  RSACrypto: "RSA-Cryptography",
  ElGamalCrypto: "ElGamal-Cryptography",
  RSASign: "RSA-Signature",
  ElGamalSign: "ElGamal-Signature",
  EllipticCurveCrypto: "Elliptic-Curve-Cryptography",
  EllipticCurveSign: "Elliptic-Curve-Signature",
});

const AlgorithmParameters = Object.freeze({
  [Algorithms.RSACrypto]: Object.freeze({
    encrypt: ["message"],
    decrypt: ["encrypted", "private_key"],
  }),
  [Algorithms.ElGamalCrypto]: Object.freeze({
    encrypt: ["message"],
    decrypt: ["encrypted", "private_key"],
  }),
  [Algorithms.RSASign]: Object.freeze({
    encrypt: ["message"],
    decrypt: ["message", "signature", "public_key"],
  }),
  [Algorithms.ElGamalSign]: Object.freeze({
    encrypt: ["message"],
    decrypt: ["message", "signature", "alpha", "beta", "p"],
  }),

  [Algorithms.EllipticCurveCrypto]: Object.freeze({
    encrypt: ["message"],
    decrypt: ["c_1", "c_2", "private_key"],
  }),
  [Algorithms.EllipticCurveSign]: Object.freeze({
    encrypt: ["message", "private_key"],
    decrypt: ["message", "signature", "public_key"],
  }),
});
const APIURLs = {
  [Algorithms.RSACrypto]: {
    encrypt: url + "/rsa-encrypt",
    decrypt: url + "/rsa-decrypt",
  },
  [Algorithms.ElGamalCrypto]: {
    encrypt: url + "/elgamal-encrypt",
    decrypt: url + "/elgamal-decrypt",
  },
  [Algorithms.RSASign]: {
    encrypt: url + "/rsa-signature",
    decrypt: url + "/rsa-verify",
  },
  [Algorithms.ElGamalSign]: {
    encrypt: url + "/elgamal-signature",
    decrypt: url + "/elgamal-verify",
  },
  [Algorithms.EllipticCurveCrypto]: {
    encrypt: url + "/ecelgamal-encrypt",
    decrypt: url + "/ecelgamal-decrypt",
  },
  [Algorithms.EllipticCurveSign]: {
    encrypt: url + "/ecdsa-signature",
    decrypt: url + "/ecdsa-verify",
  },
};

const AlgorithmKeys = Object.freeze(
  Object.fromEntries(
    Object.entries(Algorithms).map(([key, value]) => [value, key]),
  ),
);

algorithm_selector.innerText = Algorithms.RSACrypto;
const dropdownContent = document.getElementById("dropdown-content-algorithms");

Object.keys(Algorithms).forEach((key) => {
  const button = document.createElement("button");
  button.type = "button";
  button.name = Algorithms[key]; // You can use the key (e.g., "RSACrypto") or a custom name
  button.innerText = Algorithms[key].split(" ")[0]; // Extract the algorithm name, e.g., "RSA" from "RSA Cryptography"

  dropdownContent.appendChild(button);
});

const algorithms = dropdownContent.querySelectorAll("button");
algorithms.forEach((algorithm_button) => {
  algorithm_button.onclick = () => {
    // set the checkbox the default
    functionButton.innerText = "Encrypt";

    let currentAlgo = algorithm_selector.innerText;
    decryptCheckbox.checked = false;
    removeFormInputs();
    // remove second children from there
    addParameters(AlgorithmParameters[currentAlgo].encrypt);
    console.log(currentAlgo);
    console.log(AlgorithmParameters[currentAlgo]);
    algorithm_selector.innerText = algorithm_button.name;
    console.log(algorithm_selector);
  };
});

let previousJsonData = null;

exportDataBtn.onclick = () => {
  if (previousJsonData != null) {
    // Create a Blob with the content
    const blob = new Blob([JSON.stringify(previousJsonData)], {
      type: "application/json",
    });

    // Create a temporary download link
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = "data.json"; // Set the file name

    // Trigger the download by clicking the link
    link.click();

    // Clean up
    URL.revokeObjectURL(link.href);
  }
};
decryptCheckbox.addEventListener("change", () => {
  removeFormInputs();

  let currentAlgo = algorithm_selector.innerText;

  if (decryptCheckbox.checked) {
    console.log(decryptCheckbox.checked);
    functionButton.innerText = "Decrypt";
    addParameters(AlgorithmParameters[currentAlgo].decrypt);
  } else {
    functionButton.innerText = "Encrypt";
    console.log("Unchecked");

    addParameters(AlgorithmParameters[currentAlgo].encrypt);
  }
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const formData = new FormData(event.target);
  let message = jsonifyFormData(formData);
  // means it is encryption time
  //
  let currentAlgo = algorithm_selector.innerText;

  if (!decryptCheckbox.checked) {
    callApi(message, APIURLs[currentAlgo].encrypt);
  } else {
    callApi(message, APIURLs[currentAlgo].decrypt);
  }
});

function jsonifyFormData(FormData) {
  let formObject = {};
  FormData.forEach((value, key) => {
    formObject[key] = value;
  });

  return formObject;
}

function createNewParameter(parameterName) {
  let newParameter = document.createElement("input");

  newParameter.type = "text";
  newParameter.placeholder = parameterName;
  newParameter.id = parameterName.toLowerCase();
  newParameter.name = parameterName.toLowerCase();

  return newParameter;
}
function capitalizeFirstLetter(val) {
  return String(val).charAt(0).toUpperCase() + String(val).slice(1);
}

async function callApi(message, url) {
  const spinner = document.getElementById("loading-spinner");
  const overlay = document.querySelector(".overlay");
  try {
    // Hiển thị overlay và spinner
    spinner.classList.remove("hidden");
    overlay.classList.remove("hidden");

    let data = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(message),
    });

    if (!data.ok) {
      throw new Error("Network response was not ok");
    }

    let jsonData = await data.json();
    previousJsonData = jsonData;

    let displayData = "";
    for (const key in jsonData) {
      if (jsonData.hasOwnProperty(key)) {
        displayData += `<span class="key">${capitalizeFirstLetter(key)}</span>: 
                        <div class="value">${jsonData[key]}</div><br>`;
      }
    }

    display.innerHTML = displayData;
    display.addEventListener("animationend", () => {
      display.classList.remove(animation_class);
    });
  } catch (error) {
    console.error("Error: ", error);
  } finally {
    // Ẩn overlay và spinner
    spinner.classList.add("hidden");
    overlay.classList.add("hidden");
  }

  display.classList.add(animation_class);
}


function removeFormInputs() {
  while (form.children.length >= 2) {
    form.removeChild(form.children[1]);
  }
}

function addParameters(parameters) {
  parameters.forEach((param) => {
    let newParameter = createNewParameter(param);
    form.appendChild(newParameter);
  });
}
