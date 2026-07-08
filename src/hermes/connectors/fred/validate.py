import logging

logger = logging.getLogger(__name__)


class FredValidator:

    def validate_metadata(self, data: dict):

        if "seriess" not in data:
            logger.warning("Not metadata payload")
            return []

        items = data["seriess"]

        if len(items) == 0:
            logger.error("Empty metadata payload")
            return []

        valid_items = []

        for item in items:

            required_fields = [
                "id",
                "title",
                "frequency",
                "units",
            ]

            missing_fields = [
                field
                for field in required_fields
                if field not in item
            ]

            if missing_fields:
                logger.error(
                    f"Missing fields {missing_fields} "
                    f"for series {item.get('id', 'UNKNOWN')}"
                )
                continue

            valid_items.append(item)

        return valid_items

    def validate_obs(self, data: dict):

        if "observations" not in data:
            logger.warning("Not observations payload")
            return []

        items = data["observations"]

        if len(items) == 0:
            logger.error("Empty observations payload")
            return []

        valid_items = []

        for index, item in enumerate(items):

            if "date" not in item:
                logger.info(
                    f"Observation {index} missing date. Skipping."
                )
                continue

            if "value" not in item:
                logger.info(
                    f"Observation {index} missing value. Skipping."
                )
                continue

            if item["value"] == ".":
                logger.info(
                    f"Observation {index} has missing value. Skipping."
                )
                continue

            try:
                item["value"] = float(item["value"])

            except (ValueError, TypeError):
                logger.info(
                    f"Observation {index} value "
                    f"cannot be converted to float. Skipping."
                )
                continue

            valid_items.append(item)

        return valid_items
    

    def validate(self, data: dict, endpoint: str):

        if endpoint == "metadata":
            print('Meta data has been validated')
            return self.validate_metadata(data=data)

        if endpoint == "observations":
            print('Obs has been validated')
            return self.validate_obs(data=data)

        raise ValueError(f"Unknown endpoint: {endpoint}")