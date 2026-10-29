use crate::utils::errors::NormalizationError;

pub struct Normalize {
    original_value: String,
    normalize_value: String,
}

pub fn normalize(value: String) -> Result<Normalize, NormalizationError> {
    let normalize_value = value.clone();

    let normalized_value = Normalize {
        original_value: value,
        normalize_value: normalize_value,
    };
    Ok(normalized_value)
}
