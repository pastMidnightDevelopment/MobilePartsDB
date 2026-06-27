# CHANGELOG

## v0.1.0 — Database Foundation

**Summary**

Initial backend implementation for MobilePartsDB.

**Changes**

* Created SQLite database.
* Added entry creation and retrieval.
* Added database reset utility.
* Established initial project structure.

**Status**

✔ Stable

---

## v0.2.0 — Attachment Storage

**Summary**

Implemented attachment storage architecture and automatic file organization.

**Changes**

* Added support for multiple attachments per entry.
* Implemented automatic entry folders.
* Added sequential attachment naming.
* Switched to relative file paths for cross-platform compatibility.

**Status**

✔ Stable

---

## v0.3.0 — Attachment Architecture

**Summary**

Refactored the backend to support a generalized attachment system for future expansion.

**Changes**

* Replaced photo-based architecture with attachment-based architecture.
* Renamed database table from `photos` to `attachments`.
* Added attachment file type support.
* Prepared backend for images, videos, audio, PDFs, and documents.
* Improved portability for future integration with the Memory App.

**Status**

✔ Stable
