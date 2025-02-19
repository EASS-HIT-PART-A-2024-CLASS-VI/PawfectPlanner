import { useState } from "react";

function PetProfile() {
  const [step, setStep] = useState(1);
  const [petData, setPetData] = useState({
    name: "",
    type: "Dog",
    breed: "",
    age: "",
    weight: "",
    healthIssues: "",
    behaviorIssues: "",
  });

  const handleChange = (e) => {
    setPetData({ ...petData, [e.target.name]: e.target.value });
  };

  return (
    <div>
      <h2>Enter Pet Profile</h2>
      {step === 1 && (
        <>
          <label>Pet Name:</label>
          <input
            type="text"
            name="name"
            value={petData.name}
            onChange={handleChange}
          />
          <button onClick={() => setStep(2)}>Next</button>
        </>
      )}

      {step === 2 && (
        <>
          <label>Pet Type:</label>
          <select name="type" value={petData.type} onChange={handleChange}>
            <option value="Dog">Dog</option>
            <option value="Cat">Cat</option>
            <option value="Other">Other</option>
          </select>
          <button onClick={() => setStep(3)}>Next</button>
        </>
      )}

      {step === 3 && (
        <>
          <label>Breed:</label>
          <input
            type="text"
            name="breed"
            value={petData.breed}
            onChange={handleChange}
            placeholder="Type or select a breed"
          />
          <button onClick={() => setStep(4)}>Next</button>
        </>
      )}

      {step === 4 && (
        <>
          <label>Age (Years):</label>
          <input
            type="number"
            name="age"
            value={petData.age}
            onChange={handleChange}
          />
          <button onClick={() => setStep(5)}>Next</button>
        </>
      )}

      {step === 5 && (
        <>
          <label>Weight (kg):</label>
          <input
            type="number"
            name="weight"
            value={petData.weight}
            onChange={handleChange}
          />
          <button onClick={() => setStep(6)}>Next</button>
        </>
      )}

      {step === 6 && (
        <>
          <label>Health Issues:</label>
          <textarea
            name="healthIssues"
            value={petData.healthIssues}
            onChange={handleChange}
          ></textarea>
          <button onClick={() => setStep(7)}>Next</button>
        </>
      )}

      {step === 7 && (
        <>
          <label>Behavior Issues:</label>
          <textarea
            name="behaviorIssues"
            value={petData.behaviorIssues}
            onChange={handleChange}
          ></textarea>
          <button onClick={() => console.log("Saved Pet:", petData)}>
            Save Profile
          </button>
        </>
      )}
    </div>
  );
}

export default PetProfile;
