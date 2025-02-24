import { useState } from 'react';
import './Treatments.css';

const dogVaccines = ['Rabies', 'Parvovirus', 'Distemper'];
const catVaccines = ['Feline Leukemia', 'Rabies', 'Calicivirus'];

function Treatments() {
  const [petType, setPetType] = useState('Dog');

  return (
    <div className="treatments-container">
      <h2>Recommended Treatments</h2>
      <label>Pet Type:</label>
      <select value={petType} onChange={(e) => setPetType(e.target.value)}>
        <option value="Dog">Dog</option>
        <option value="Cat">Cat</option>
      </select>

      <h3>Vaccines:</h3>
      <ul>
        {(petType === 'Dog' ? dogVaccines : catVaccines).map((vaccine, index) => (
          <li key={index}>{vaccine}</li>
        ))}
      </ul>
    </div>
  );
}

export default Treatments;
