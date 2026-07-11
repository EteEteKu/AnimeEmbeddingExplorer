const API_BASE_URL = "http://127.0.0.1:8000";

const searchInput = document.getElementById("search-input");
const searchResults = document.getElementById("search-results");
const similarResults = document.getElementById("similar-results");
const cloudViewport = document.getElementById("cloud-viewport");
const emptyCloudHint = document.getElementById("empty-cloud-hint");

let currentCenterAnime = null;
let panX = 0, panY = 0, scale = 1;
let isDragging = false;
let dragStartX = 0, dragStartY = 0;
let dragDistance = 0;


function createAnimeCard(anime, showSimilarity = false) {
	const card = document.createElement("div");
	card.className = "anime-card";

	const img = document.createElement("img");
	img.src = anime.image_url;
	img.alt = anime.name;

	const info = document.createElement("div");
	info.className = "info";

	const name = document.createElement("div");
	name.className = "name";
	name.textContent = anime.name;

	const meta = document.createElement("div");
	meta.className = "meta";
	const episodesText = anime.episodes ? `${Math.trunc(anime.episodes)} эп.` : "";
	meta.textContent = `${anime.genres} · ${episodesText} · ★ ${anime.score}`;

	info.appendChild(name);
	info.appendChild(meta);
	card.appendChild(img);
	card.appendChild(info);

	if (showSimilarity && anime.total_sim !== undefined) {
		const sim = document.createElement("div");
		sim.className = "similarity";
		sim.textContent = `${Math.round(anime.total_sim * 100)}%`;
		card.appendChild(sim);
	}

	card.addEventListener("click", () => {
		if (dragDistance > 5) return;
		selectAnime(anime);
	});

	return card;
}


function renderSearchResults(animeList) {
	searchResults.innerHTML = "";

	if (!animeList || animeList.length === 0) {
		searchResults.innerHTML = `<div class="empty-state">Ничего не найдено</div>`;
		return;
	}

	animeList.forEach(anime => {
		const card = createAnimeCard(anime);
		searchResults.appendChild(card);
	});
}

async function searchAnime(query) {
	if (!query || query.trim().length < 2) {
		searchResults.innerHTML = "";
		return;
	}

	try {
		const url = `${API_BASE_URL}/anime/search?anime_name=${encodeURIComponent(query)}&limit=8`;
		const response = await fetch(url);

		if (!response.ok) {
			throw new Error(`Сервер ответил ошибкой: ${response.status}`);
		}

		const data = await response.json();
		renderSearchResults(data.found);
	} catch (err) {
		console.error("Ошибка при поиске:", err);
		searchResults.innerHTML = `<div class="empty-state">Не удалось связаться с сервером</div>`;
	}
}

let debounceTimer = null;
function debounce(fn, delay) {
	return (...args) => {
		clearTimeout(debounceTimer);
		debounceTimer = setTimeout(() => fn(...args), delay);
	};
}

searchInput.addEventListener("input", debounce((e) => {
	searchAnime(e.target.value);
}, 350));


function selectAnime(anime) {
	currentCenterAnime = anime;

	searchInput.value = "";
	searchResults.innerHTML = "";

	fetchSimilarAnime(anime.anime_id);
}

async function fetchSimilarAnime(animeId) {
	emptyCloudHint.classList.add("hidden");
	similarResults.innerHTML = `<div class="empty-state">Загрузка...</div>`;

	try {
		const response = await fetch(`${API_BASE_URL}/anime/similar`, {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({
				anime_id: animeId,
				limit: 12,
				min_similarity: 0.4
			})
		});

		if (!response.ok) {
			throw new Error(`Сервер ответил ошибкой: ${response.status}`);
		}

		const data = await response.json();
		renderCloud(currentCenterAnime, data.similar);
	} catch (err) {
		console.error("Ошибка при получении похожих:", err);
		similarResults.innerHTML = `<div class="empty-state">Не удалось загрузить похожие тайтлы</div>`;
	}
}


function renderCloud(centerAnime, animeList) {
	similarResults.innerHTML = "";
	panX = 0; panY = 0; scale = 0.5;
	updateCloudTransform();

	const svgNS = "http://www.w3.org/2000/svg";
	const svg = document.createElementNS(svgNS, "svg");
	svg.classList.add("cloud-edges");
	svg.setAttribute("width", "100%");
	svg.setAttribute("height", "100%");

	const defs = document.createElementNS(svgNS, "defs");
	similarResults.appendChild(svg);
	svg.appendChild(defs);

	const centerCard = createAnimeCard(centerAnime, false);
	centerCard.classList.add("center-card");
	centerCard.style.left = `50%`;
	centerCard.style.top = `50%`;
	similarResults.appendChild(centerCard);

	if (!animeList || animeList.length === 0) return;

	const sims = animeList.map(a => a.total_sim);
	const minSim = Math.min(...sims);
	const maxSim = Math.max(...sims);
	const simRange = maxSim - minSim || 1;

	const GOLDEN_ANGLE = 137.5 * (Math.PI / 180);
	const minRadius = 260;
	const maxRadius = 750;

	animeList.forEach((anime, index) => {
		const angle = index * GOLDEN_ANGLE + (Math.random() - 0.5) * 0.25;
		const normalizedSim = (anime.total_sim - minSim) / simRange;
		const baseRadius = minRadius + (1 - normalizedSim) * (maxRadius - minRadius);
		const radius = baseRadius + (Math.random() - 0.5) * 10;

		const x = radius * Math.cos(angle);
		const y = radius * Math.sin(angle);

		const gradientId = `edgeGrad${index}`;
		const gradient = document.createElementNS(svgNS, "linearGradient");
		gradient.setAttribute("id", gradientId);
		gradient.setAttribute("x1", "50%");
		gradient.setAttribute("y1", "50%");
		gradient.setAttribute("x2", `${50 + (x / 20)}%`);
		gradient.setAttribute("y2", `${50 + (y / 14)}%`);

		const stop1 = document.createElementNS(svgNS, "stop");
		stop1.setAttribute("offset", "0%");
		stop1.setAttribute("stop-color", "#7c6fff");
		stop1.setAttribute("stop-opacity", 0.5 * normalizedSim + 0.15);

		const stop2 = document.createElementNS(svgNS, "stop");
		stop2.setAttribute("offset", "100%");
		stop2.setAttribute("stop-color", "#7c6fff");
		stop2.setAttribute("stop-opacity", 0);

		gradient.appendChild(stop1);
		gradient.appendChild(stop2);
		defs.appendChild(gradient);

		const line = document.createElementNS(svgNS, "line");
		line.setAttribute("x1", "50%");
		line.setAttribute("y1", "50%");
		line.setAttribute("x2", `calc(50% + ${x}px)`);
		line.setAttribute("y2", `calc(50% + ${y}px)`);
		line.setAttribute("stroke", `url(#${gradientId})`);
		line.setAttribute("stroke-width", 1.5);
		svg.appendChild(line);

		const card = createAnimeCard(anime, true);
		card.style.left = `calc(50% + ${x}px)`;
		card.style.top = `calc(50% + ${y}px)`;
		similarResults.appendChild(card);
	});
}


function updateCloudTransform() {
	similarResults.style.transform = `translate(${panX}px, ${panY}px) scale(${scale})`;
}

cloudViewport.addEventListener("mousedown", (e) => {
	isDragging = true;
	dragDistance = 0;
	cloudViewport.classList.add("dragging");
	dragStartX = e.clientX - panX;
	dragStartY = e.clientY - panY;
});

window.addEventListener("mousemove", (e) => {
	if (!isDragging) return;
	const newPanX = e.clientX - dragStartX;
	const newPanY = e.clientY - dragStartY;
	dragDistance += Math.abs(newPanX - panX) + Math.abs(newPanY - panY);
	panX = newPanX;
	panY = newPanY;
	updateCloudTransform();
});

window.addEventListener("mouseup", () => {
	isDragging = false;
	cloudViewport.classList.remove("dragging");
});


cloudViewport.addEventListener("wheel", (e) => {
    e.preventDefault();
	const zoomIntensity = 0.001;
	scale = Math.min(2.5, Math.max(0.3, scale - e.deltaY * zoomIntensity));
	updateCloudTransform();
});