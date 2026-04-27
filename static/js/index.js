const loadAnimalsButton = document.getElementById("load-animals");
const animalsPrevButton = document.getElementById("animals-prev");
const animalsNextButton = document.getElementById("animals-next");
const animalsViewport = document.getElementById("animals-viewport");
const animalsList = document.getElementById("animals-list");
const animalsFeedback = document.getElementById("animals-feedback");

function setFeedback(element, message, type) {
  element.textContent = message;
  element.classList.remove("feedback--ok", "feedback--error");
  if (type) {
    element.classList.add(type === "ok" ? "feedback--ok" : "feedback--error");
  }
}

function formatDate(dateValue) {
  if (!dateValue) {
    return "-";
  }

  const [year, month, day] = dateValue.split("-");
  if (!year || !month || !day) {
    return dateValue;
  }

  return `${day}/${month}/${year}`;
}

function getStatusVariant(status) {
  return status === "disponivel" ? "animal-card__status--disponivel" : "animal-card__status--nao-disponivel";
}

function getAnimalsPayload(payload) {
  if (Array.isArray(payload)) {
    return payload;
  }
  if (payload && Array.isArray(payload.results)) {
    return payload.results;
  }
  return [];
}

function createInfoRow(label, content) {
  const paragraph = document.createElement("p");
  const strong = document.createElement("span");
  strong.className = "animal-card__label";
  strong.textContent = `${label}: `;
  paragraph.appendChild(strong);
  paragraph.append(content);
  return paragraph;
}

function buildAnimalCard(animal) {
  const item = document.createElement("li");
  item.className = "animal-card";

  const title = document.createElement("h3");
  title.textContent = animal.raca || "Raça não informada";
  item.appendChild(title);

  const statusBadge = document.createElement("span");
  statusBadge.className = `animal-card__status ${getStatusVariant(animal.status)}`;
  statusBadge.textContent = animal.status_display || animal.status || "Sem status";

  item.appendChild(createInfoRow("Status", statusBadge));
  item.appendChild(createInfoRow("Acolhimento", formatDate(animal.data_acolhimento)));
  item.appendChild(createInfoRow("Adoção", animal.data_adocao ? formatDate(animal.data_adocao) : "Ainda não adotado"));

  return item;
}

function setCarouselEnabled(enabled) {
  animalsPrevButton.disabled = !enabled;
  animalsNextButton.disabled = !enabled;
}

function scrollAnimals(direction) {
  const step = animalsViewport.clientWidth * 0.85;
  animalsViewport.scrollBy({
    left: step * direction,
    behavior: "smooth"
  });
}

async function loadAnimals() {
  setFeedback(animalsFeedback, "Carregando animais...", null);
  animalsList.innerHTML = "";
  setCarouselEnabled(false);

  const url = new URL("/api/animals/", window.location.origin);
  url.searchParams.set("disponivel", "true");

  try {
    const response = await fetch(url);
    const payload = await response.json().catch(() => ({}));

    if (!response.ok) {
      throw new Error("Erro ao carregar os animais.");
    }

    const animals = getAnimalsPayload(payload);
    if (animals.length === 0) {
      setFeedback(animalsFeedback, "Nenhum animal disponível para adoção no momento.", null);
      return;
    }

    animals.forEach((animal) => {
      animalsList.appendChild(buildAnimalCard(animal));
    });

    setCarouselEnabled(true);
    setFeedback(animalsFeedback, `Lista atualizada com ${animals.length} animal(is).`, "ok");
  } catch (error) {
    setFeedback(animalsFeedback, error.message, "error");
  }
}

loadAnimalsButton.addEventListener("click", loadAnimals);
animalsPrevButton.addEventListener("click", () => scrollAnimals(-1));
animalsNextButton.addEventListener("click", () => scrollAnimals(1));
loadAnimals();
