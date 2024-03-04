-- CreateTable
CREATE TABLE "RuralPropertyAgrotoxic" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "rural_property_id" INTEGER NOT NULL,
    "agrotoxic_id" INTEGER NOT NULL,
    CONSTRAINT "RuralPropertyAgrotoxic_rural_property_id_fkey" FOREIGN KEY ("rural_property_id") REFERENCES "RuralProperty" ("id") ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT "RuralPropertyAgrotoxic_agrotoxic_id_fkey" FOREIGN KEY ("agrotoxic_id") REFERENCES "Agrotoxic" ("id") ON DELETE CASCADE ON UPDATE CASCADE
);

-- CreateIndex
CREATE UNIQUE INDEX "RuralPropertyAgrotoxic_rural_property_id_agrotoxic_id_key" ON "RuralPropertyAgrotoxic"("rural_property_id", "agrotoxic_id");
