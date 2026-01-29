document.addEventListener('DOMContentLoaded', function () {
    // Top Level Pages
    const landingPage = document.getElementById('landingPage');
    const surveyIntroPage = document.getElementById('surveyIntroPage');
    const surveyFormPage = document.getElementById('surveyFormPage');

    // Buttons to switch pages
    const viewSurveyBtn = document.getElementById('viewSurveyBtn');
    const startSurveyBtn = document.getElementById('startSurveyBtn');

    // Form Steps (internal to Survey Page)
    const steps = document.querySelectorAll('.form-step');
    const form = document.getElementById('surveyForm');
    const progressBar = document.getElementById('progressBar');
    // State Management via URL Hash (Robust against Ctrl+F5)
    function setActivePageFromHash() {
        const hash = window.location.hash;

        // Default to landing page
        let targetId = 'landingPage';

        if (hash === '#intro') targetId = 'surveyIntroPage';
        else if (hash === '#survey') targetId = 'surveyFormPage';

        // Hide all
        [landingPage, surveyIntroPage, surveyFormPage].forEach(page => {
            if (page) {
                page.style.display = 'none';
                page.classList.remove('active');
            }
        });

        // Show target
        const targetPage = document.getElementById(targetId);
        if (targetPage) {
            targetPage.style.display = 'flex';
            targetPage.classList.add('active'); // CSS flex

            // Context-aware styling (Hybrid Footer)
            if (targetId === 'landingPage') {
                document.body.classList.add('landing-mode');
            } else {
                document.body.classList.remove('landing-mode');
            }

            // Ensure hash matches (for initial load consistency or default)
            if (targetId === 'landingPage' && hash !== '' && hash !== '#home') {
                history.replaceState(null, null, ' '); // Clean URL for landing
            } else if (targetId === 'surveyIntroPage' && hash !== '#intro') {
                history.replaceState(null, null, '#intro');
            } else if (targetId === 'surveyFormPage' && hash !== '#survey') {
                history.replaceState(null, null, '#survey');
            }
        }
    }

    // Initialize on Load
    setActivePageFromHash();

    // Handle Browser Back/Forward buttons
    window.addEventListener('hashchange', setActivePageFromHash);

    // Navigation: Landing -> Intro
    if (viewSurveyBtn) {
        viewSurveyBtn.addEventListener('click', () => {
            window.location.hash = 'intro';
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }

    // Navigation: Intro -> Form
    if (startSurveyBtn) {
        startSurveyBtn.addEventListener('click', () => {
            // Set hash to trigger view change
            window.location.hash = 'survey';

            // Wait slightly for view to change then init step
            setTimeout(() => {
                currentStepIndex = 0; // Reset index to Avoid Validation Errors
                showStep(0);
                window.scrollTo({ top: 0, behavior: 'smooth' });
            }, 50);
        });
    }

    // Initialize Progress (hidden until form starts)
    // updateProgress(); // Moved to showStep to avoid error if hidden
    const totalSteps = steps.length;
    let currentStepIndex = 0;

    // Navigation Buttons
    document.querySelectorAll('.btn-next').forEach(button => {
        button.addEventListener('click', () => {
            if (validateStep(currentStepIndex)) {
                if (currentStepIndex < totalSteps - 1) {
                    currentStepIndex++;
                    showStep(currentStepIndex);
                    window.scrollTo({ top: 0, behavior: 'smooth' });
                }
            }
        });
    });

    document.querySelectorAll('.btn-prev').forEach(button => {
        button.addEventListener('click', () => {
            if (currentStepIndex > 0) {
                currentStepIndex--;
                showStep(currentStepIndex);
                window.scrollTo({ top: 0, behavior: 'smooth' });
            }
        });
    });

    // Show Step Function
    function showStep(index) {
        steps.forEach((step, i) => {
            step.classList.toggle('active', i === index);
        });
        updateProgress();
    }

    // Update Progress Bar
    function updateProgress() {
        const percentage = ((currentStepIndex + 1) / totalSteps) * 100;
        progressBar.style.width = percentage + '%';
    }

    // Validation Logic
    function validateStep(index) {
        const currentStep = steps[index];
        const inputs = currentStep.querySelectorAll('input[required], select[required], textarea[required]');
        let valid = true;

        inputs.forEach(input => {
            if (!input.value || (input.type === 'radio' && !currentStep.querySelector(`input[name="${input.name}"]:checked`))) {
                valid = false;
                input.reportValidity();
            }
        });

        // Section B Checkboxes
        if (index === 1) {
            const checked = document.querySelectorAll('#platforms_used input[type="checkbox"]:checked');
            const errorMsg = document.getElementById('platforms_error');
            if (checked.length === 0) {
                if (errorMsg) errorMsg.style.display = 'flex';
                valid = false;
            } else {
                if (errorMsg) errorMsg.style.display = 'none';
            }
        }

        // Section D Checkboxes
        if (index === 3) {
            const checked = document.querySelectorAll('#product_categories input[type="checkbox"]:checked');
            const errorMsg = document.getElementById('categories_error');
            if (checked.length === 0) {
                if (errorMsg) errorMsg.style.display = 'flex';
                valid = false;
            } else {
                if (errorMsg) errorMsg.style.display = 'none';
            }
        }

        // Price Sensitivity Verification (Inline)
        if (index === 4) {
            const priceInput = document.getElementById('price_sensitivity');
            if (priceInput) {
                const isValid = validatePrice(priceInput);
                if (!isValid) valid = false;
            }
        }

        return valid;
    }

    // Helper: Validate Price Field
    function validatePrice(input) {
        const val = parseInt(input.value, 10);
        const errorMsg = document.getElementById('price_error');

        if (isNaN(val) || val < 1 || val > 5) {
            input.classList.add('input-error');
            if (errorMsg) errorMsg.style.display = 'flex';
            return false;
        } else {
            input.classList.remove('input-error');
            if (errorMsg) errorMsg.style.display = 'none';
            return true;
        }
    }

    // Real-time Validation for Price Sensitivity (Blur)
    const priceSensitivityInput = document.getElementById('price_sensitivity');
    if (priceSensitivityInput) {
        priceSensitivityInput.addEventListener('blur', function () {
            if (this.value !== '') {
                validatePrice(this);
            }
        });

        priceSensitivityInput.addEventListener('input', function () {
            this.classList.remove('input-error');
            const errorMsg = document.getElementById('price_error');
            if (errorMsg) errorMsg.style.display = 'none';
        });
    }

    // Toggle "Others" input for Platforms
    const platformCheckboxes = document.querySelectorAll('#platforms_used input[type="checkbox"]');
    const otherContainer = document.getElementById('other_platform_container');
    const otherInput = document.getElementById('other_platform_name');

    platformCheckboxes.forEach(cb => {
        cb.addEventListener('change', (e) => {
            // Check if "Others" checkbox is involved
            if (e.target.value === 'Others') {
                if (e.target.checked) {
                    otherContainer.style.display = 'block';
                    otherInput.required = true;
                } else {
                    otherContainer.style.display = 'none';
                    otherInput.required = false;
                    otherInput.value = '';
                }
            }
        });
    });

    // Form Submission
    form.addEventListener('submit', async function (e) {
        e.preventDefault();
        console.log("Form submission attempted.");

        // Final validation
        if (!validateStep(currentStepIndex)) {
            console.warn("Validation failed on step " + currentStepIndex);
            // Shake the form or show a generic toast if needed, but reportValidity should handle it.
            // Force focus on the first invalid input just in case
            const currentStep = steps[currentStepIndex];
            const invalidInput = currentStep.querySelector(':invalid');
            if (invalidInput) invalidInput.focus();
            return;
        }

        console.log("Validation passed. Submitting...");
        const submitBtn = document.getElementById('submitBtn');
        const errorMsg = document.getElementById('error-message');

        submitBtn.disabled = true;
        submitBtn.textContent = "Submitting...";
        errorMsg.style.display = 'none';

        // Helpers
        const getCheckedValues = (groupId) => {
            const checkboxes = document.querySelectorAll(`#${groupId} input[type="checkbox"]:checked`);
            return Array.from(checkboxes).map(cb => cb.value);
        };
        const getRadioValue = (name) => {
            const radio = document.querySelector(`input[name="${name}"]:checked`);
            return radio ? radio.value : null;
        };

        // Construct Payload
        const formData = {
            full_name: document.getElementById('full_name').value,
            email: document.getElementById('email').value,
            age_group: document.getElementById('age_group').value,
            household_type: document.getElementById('household_type').value,

            awareness: getRadioValue('awareness') === 'true',

            platforms_used: getCheckedValues('platforms_used'),
            other_platform_name: document.getElementById('other_platform_name').value || null,

            most_used_platform: document.getElementById('most_used_platform').value,
            usage_frequency: document.getElementById('usage_frequency').value,

            average_order_value: document.getElementById('average_order_value').value,
            time_saved: document.getElementById('time_saved').value,

            product_categories: getCheckedValues('product_categories'),
            purchase_frequency_change: document.getElementById('purchase_frequency_change').value,
            impulse_buying: document.getElementById('impulse_buying').value,

            price_sensitivity: parseInt(document.getElementById('price_sensitivity').value, 10),

            price_comparison: document.getElementById('price_comparison').value,
            local_shops_impact: document.getElementById('local_shops_impact').value,

            importance_delivery: document.getElementById('importance_delivery').value,
            importance_convenience: document.getElementById('importance_convenience').value,
            importance_pricing: document.getElementById('importance_pricing').value,
            importance_availability: document.getElementById('importance_availability').value,

            overall_satisfaction: document.getElementById('overall_satisfaction').value,
            future_usage_intent: document.getElementById('future_usage_intent').value,

            qualitative_response: document.getElementById('qualitative_response').value || null
        };

        try {
            const response = await fetch('/submit-response', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData)
            });

            const result = await response.json();

            if (response.ok) {
                // Show Success View
                form.style.display = 'none';
                document.getElementById('successView').style.display = 'block';
                document.querySelector('.progress-container').style.display = 'none';
                window.scrollTo(0, 0);
            } else {
                let msg = result.detail || "Submission failed";
                if (Array.isArray(result.detail)) {
                    msg = "Validation Error: " + result.detail.map(e => e.msg).join(', ');
                }
                throw new Error(msg);
            }
        } catch (error) {
            errorMsg.textContent = error.message;
            errorMsg.style.display = 'block';
            submitBtn.disabled = false;
            submitBtn.textContent = "Submit Survey";
        }
    });

});
