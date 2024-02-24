-- CreateTable
CREATE TABLE "User" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "name" TEXT NOT NULL,
    "email" TEXT NOT NULL,
    "access_level" INTEGER NOT NULL DEFAULT 1,
    "bio_hash" BLOB NOT NULL
);

-- CreateTable
CREATE TABLE "RuralProperty" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "name" TEXT NOT NULL,
    "access_level" INTEGER NOT NULL DEFAULT 3
);

-- CreateTable
CREATE TABLE "Agrotoxic" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "name" TEXT NOT NULL,
    "environment_impact" TEXT NOT NULL DEFAULT 'BAIXO',
    "access_level" INTEGER NOT NULL DEFAULT 3
);

-- CreateTable
CREATE TABLE "Stock" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "agrotoxic_id" INTEGER NOT NULL,
    "access_level" INTEGER NOT NULL DEFAULT 2,
    CONSTRAINT "Stock_agrotoxic_id_fkey" FOREIGN KEY ("agrotoxic_id") REFERENCES "Agrotoxic" ("id") ON DELETE RESTRICT ON UPDATE CASCADE
);

-- CreateIndex
CREATE UNIQUE INDEX "User_email_key" ON "User"("email");

-- CreateIndex
CREATE UNIQUE INDEX "Stock_agrotoxic_id_key" ON "Stock"("agrotoxic_id");
