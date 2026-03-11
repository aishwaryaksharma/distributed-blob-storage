# 📦 BlobStore Engine

A high-performance, deduplicating Blob Storage Service built with **Django**, **DRF**, and **PostgreSQL**. This system is designed with a clear separation between the **Control Plane** (Metadata) and the **Data Plane** (Physical Storage).

## 🚀 Key Features

* **Content-Addressable Storage (CAS):** Uses SHA-256 checksums to ensure file integrity and implement automatic data deduplication.
* **Atomic Transactions:** Ensures database records and physical disk files stay in sync during creation and deletion.
* **Streaming I/O:** Handles large file uploads and downloads using streaming chunks to maintain a low memory footprint.
* **Partial UI Refresh:** A modern, "SPA-lite" dashboard for managing blobs without full page reloads.
* **Permanent Deletion:** Synchronized cleanup of both database entries and physical storage.

---

## 🏗️ System Architecture

The project follows a **Domain-Driven Design (DDD)** approach with isolated layers for models, views, and business logic (services).

---

## 🛠️ API Documentation

| Endpoint | Method | Description | Key Parameters | Success Status |
| :--- | :--- | :--- | :--- | :--- |
| `/` | `GET` | **Dashboard UI**: Management interface. | None | `200 OK` |
| `/api/upload/` | `POST` | **Upload Blob**: Streams file to storage. | `file` (Multipart) | `201 Created` |
| `/api/list/` | `GET` | **List Blobs**: Retrieves latest 10 files. | None | `200 OK` |
| `/api/download/<uuid>/` | `GET` | **Download Blob**: Streams bytes to client. | `blob_id` (UUID) | `200 OK` |
| `/api/delete/<uuid>/` | `DELETE` | **Permanent Delete**: Removes from disk/DB. | `blob_id` (UUID) | `204 No Content` |

---

### Tech Stack
* **Language:** Python 3.10+
* **Framework:** Django 4.x / Django REST Framework
* **Database:** PostgreSQL (running in Docker)
* **Frontend:** Vanilla JavaScript (Fetch API / XHR for progress tracking)

## 📈 Important Considerations
* **Scalability:** Currently utilizes local disk storage. The BlobUploadService is designed to be easily refactored to support S3 or Google Cloud Storage by swapping the storage driver.
* **Data Integrity:** Implements checksum verification to prevent file corruption during transport.
* **Security:** UUIDs are used for all public-facing identifiers to prevent ID enumeration/crawling attacks.
---

## 🛠️ Getting Started

### 1. Database Setup (Docker)
Run the PostgreSQL container with the dedicated database:
```bash
docker run --name blobstore-docker \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=blobstore_db \
  -p 5432:5432 \
  -d postgres
```

### 2. Installation
```bash
# Clone the repository and install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations
python manage.py migrate
```

### 3. Running the Server
```bash
python manage.py runserver
```

### 4. Access the dashboard 
http://127.0.0.1:8000/

