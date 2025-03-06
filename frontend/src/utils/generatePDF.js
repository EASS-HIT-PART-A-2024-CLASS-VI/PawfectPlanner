// File: frontend/src/utils/generatePDF.js
import jsPDF from "jspdf";
import { differenceInYears } from "date-fns";

export const generatePetPDF = (pet) => {
  if (!pet) {
    console.error("Pet data is missing.");
    return;
  }

  const doc = new jsPDF();

  doc.setFontSize(22);
  doc.text(`${pet.name}'s Pet Profile`, 20, 20);

  doc.setFontSize(16);
  let currentY = 40;

  // Breed
  doc.text(`Breed: ${pet.breed}`, 20, currentY);
  currentY += 10;

  // If we have a birth_date, show it + approximate age
  if (pet.birth_date) {
    const birth = new Date(pet.birth_date);
    let ageYears = "";
    try {
      ageYears = differenceInYears(new Date(), birth);
    } catch (err) {
      // ignore
    }
    doc.text(
      `Birth Date: ${birth.toLocaleDateString()}${
        ageYears ? ` (Age ~ ${ageYears})` : ""
      }`,
      20,
      currentY
    );
    currentY += 10;
  }

  // Weight
  const displayWeight = pet.weight == null ? "not defined" : `${pet.weight} kg`;
  doc.text(`Weight: ${displayWeight}`, 20, currentY);
  currentY += 10;

  // Life expectancy
  if (pet.life_expectancy) {
    doc.text(`Life Expectancy: ${pet.life_expectancy}`, 20, currentY);
    currentY += 10;
  }

  // Health issues
  if (pet.health_issues && pet.health_issues.length > 0) {
    const healthStr = Array.isArray(pet.health_issues)
      ? pet.health_issues.join(", ")
      : pet.health_issues;
    doc.text(`Health Issues: ${healthStr}`, 20, currentY);
    currentY += 10;
  }

  // Behavior issues
  if (pet.behavior_issues && pet.behavior_issues.length > 0) {
    const behaviorStr = Array.isArray(pet.behavior_issues)
      ? pet.behavior_issues.join(", ")
      : pet.behavior_issues;
    doc.text(`Behavior Issues: ${behaviorStr}`, 20, currentY);
    currentY += 10;
  }

  // Recommended weight range
  if (pet.average_weight_range && pet.average_weight_range !== "Unknown") {
    doc.text(`Recommended Weight Range: ${pet.average_weight_range} kg`, 20, currentY);
    currentY += 10;

    // Check if the weight is far from recommended
    if (pet.weight) {
      const rangeStr = pet.average_weight_range.replace(/\s*kg\s*/gi, "");
      const parts = rangeStr.split("-").map((p) => p.trim());
      if (parts.length === 2) {
        const minVal = parseFloat(parts[0]);
        const maxVal = parseFloat(parts[1]);
        if (!isNaN(minVal) && !isNaN(maxVal)) {
          const lower = minVal * 0.8;
          const upper = maxVal * 1.2;
          if (pet.weight < lower || pet.weight > upper) {
            doc.setTextColor(255, 0, 0);
            doc.text("Weight is far from the breed's average!", 20, currentY);
            doc.setTextColor(0, 0, 0);
            currentY += 10;
          }
        }
      }
    }
  }

  // Bred for + breed group
  if (pet.bred_for) {
    doc.text(`Bred For: ${pet.bred_for}`, 20, currentY);
    currentY += 10;
  }
  if (pet.breed_group) {
    doc.text(`Breed Group: ${pet.breed_group}`, 20, currentY);
    currentY += 10;
  }

  doc.save(`${pet.name}_profile.pdf`);
};
