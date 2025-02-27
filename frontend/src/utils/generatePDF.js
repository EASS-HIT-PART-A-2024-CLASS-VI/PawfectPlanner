// src/utils/generatePDF.js
import jsPDF from "jspdf";

export const generatePetPDF = (pet) => {
  if (!pet) {
    console.error("Pet data is missing.");
    return;
  }

  const doc = new jsPDF();
  doc.setFontSize(22);
  doc.text(`${pet.name}'s Pet Profile`, 20, 20);
  doc.setFontSize(16);
  doc.text(`Breed: ${pet.breed}`, 20, 40);

  if (pet.breed_info) {
    doc.text(`Life Expectancy: ${pet.breed_info.life_expectancy}`, 20, 50);
    doc.text(`Temperament: ${pet.breed_info.temperament}`, 20, 60);
    doc.text(`Health Issues: ${pet.breed_info.health_issues}`, 20, 70);
    doc.text(`Weight: ${pet.weight} kg`, 20, 80);
    
    if (pet.breed_info.average_weight) {
      doc.text(`Recommended Weight: ${pet.breed_info.average_weight} kg`, 20, 90);
    }

    if (
      pet.weight > parseFloat(pet.breed_info.average_weight) * 1.2 ||
      pet.weight < parseFloat(pet.breed_info.average_weight) * 0.8
    ) {
      doc.setTextColor(255, 0, 0); // Red color for warning
      doc.text("⚠️ Weight is outside the recommended range!", 20, 100);
    }
  }

  doc.save(`${pet.name}_profile.pdf`);
};