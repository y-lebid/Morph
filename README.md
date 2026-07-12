# 🌐 Morph

**Morph** is a custom browser builder based on the Chromium engine and Python (PyQt6). 

The main idea behind the project: the browser isn’t a monolith. It’s just a “core” that can render pages, while all additional functionality (AI agents, terminals, custom parsers) is added via simple Python scripts as plugins.

## 🚀 Key Features (in the works)
* **Chromium under the hood:** Fast and modern page rendering.
* **Open plugin architecture:** Anyone can write a `.py` file, drop it into the `plugins` folder, and the browser will gain a new feature.
* **Python-native:** The ideal environment for integrating machine learning, data processing, and automation.
* **GitHub Sync:** The ability to sync your settings and plugins directly from a repository.

## 🛠️ Technology Stack
* Python 3.10+
* PyQt6
* PyQt6-WebEngine (Chromium)
