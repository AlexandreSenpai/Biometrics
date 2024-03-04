-- RedefineTables
PRAGMA foreign_keys=OFF;
CREATE TABLE "new_Stock" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "agrotoxic_id" INTEGER NOT NULL,
    "quantity" INTEGER NOT NULL DEFAULT 0,
    "access_level" INTEGER NOT NULL DEFAULT 2,
    CONSTRAINT "Stock_agrotoxic_id_fkey" FOREIGN KEY ("agrotoxic_id") REFERENCES "Agrotoxic" ("id") ON DELETE RESTRICT ON UPDATE CASCADE
);
INSERT INTO "new_Stock" ("access_level", "agrotoxic_id", "id") SELECT "access_level", "agrotoxic_id", "id" FROM "Stock";
DROP TABLE "Stock";
ALTER TABLE "new_Stock" RENAME TO "Stock";
CREATE UNIQUE INDEX "Stock_agrotoxic_id_key" ON "Stock"("agrotoxic_id");
PRAGMA foreign_key_check;
PRAGMA foreign_keys=ON;
