document.addEventListener('DOMContentLoaded', function() {
    // Show/hide password toggle
    const togglePassword = document.querySelector('#togglePassword');
    const password = document.querySelector('#password');

    if (togglePassword && password) {
        togglePassword.addEventListener('click', function (e) {
            // toggle the type attribute
            const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
            password.setAttribute('type', type);
            // toggle the eye slash icon
            this.textContent = this.textContent === 'Show' ? 'Hide' : 'Show';
        });
    }

    // Client-side form validation for create/edit shipment
    const shipmentForm = document.querySelector('#createShipmentForm, #editShipmentForm');
    if (shipmentForm) {
        shipmentForm.addEventListener('submit', function(event) {
            const baseCost = document.querySelector('#base_cost');
            const taxRate = document.querySelector('#tax_rate');
            const handlingFee = document.querySelector('#handling_fee');

            if (baseCost && (isNaN(parseFloat(baseCost.value)) || !isFinite(baseCost.value) || parseFloat(baseCost.value) < 0)) {
                alert('Base Cost must be a non-negative number.');
                event.preventDefault();
                return;
            }
            if (taxRate && (isNaN(parseFloat(taxRate.value)) || !isFinite(taxRate.value) || parseFloat(taxRate.value) < 0 || parseFloat(taxRate.value) > 1)) {
                alert('Tax Rate must be a number between 0 and 1.');
                event.preventDefault();
                return;
            }
            if (handlingFee && (isNaN(parseFloat(handlingFee.value)) || !isFinite(handlingFee.value) || parseFloat(handlingFee.value) < 0)) {
                alert('Handling Fee must be a non-negative number.');
                event.preventDefault();
                return;
            }
        });
    }
});