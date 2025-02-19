import './VetLocator.css';

function VetLocator() {
  const openVetSearch = () => {
    window.open('https://www.google.com/maps/search/Veterinary+clinic', '_blank');
  };

  return (
    <div className="vet-container">
      <h2>Find a Vet Near You</h2>
      <button onClick={openVetSearch} className="vet-button">
        Open Google Maps
      </button>
    </div>
  );
}

export default VetLocator;
