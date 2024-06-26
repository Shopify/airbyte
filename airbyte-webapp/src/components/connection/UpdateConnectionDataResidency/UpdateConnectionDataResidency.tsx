import React, { useState } from "react";
import { FormattedMessage, useIntl } from "react-intl";

import { DataGeographyDropdown } from "components/common/DataGeographyDropdown";
import { ControlLabels } from "components/LabeledControl";
import { Card } from "components/ui/Card";
import { Spinner } from "components/ui/Spinner";

import { Geography } from "core/request/AirbyteClient";
import { useConnectionEditService } from "hooks/services/ConnectionEdit/ConnectionEditService";
import { useNotificationService } from "hooks/services/Notification";
import { useAvailableGeographies } from "packages/cloud/services/geographies/GeographiesService";
import { links } from "utils/links";

import styles from "./UpdateConnectionDataResidency.module.scss";

export const UpdateConnectionDataResidency: React.FC = () => {
  const { connection, updateConnection, connectionUpdating } = useConnectionEditService();
  const { registerNotification } = useNotificationService();
  const { formatMessage } = useIntl();
  const [selectedValue, setSelectedValue] = useState<Geography>();

  const { geographies } = useAvailableGeographies();

  const handleSubmit = async (value: Geography) => {
    try {
      setSelectedValue(value);
      await updateConnection({
        connectionId: connection.connectionId,
        geography: value,
      });
    } catch (e) {
      registerNotification({
        id: "connection.geographyUpdateError",
        title: formatMessage({ id: "connection.geographyUpdateError" }),
        isError: true,
      });
    }
    setSelectedValue(undefined);
  };

  return (
    <Card withPadding>
      <div className={styles.wrapper}>
        <div>
          <ControlLabels
            nextLine
            label={<FormattedMessage id="connection.geographyTitle" />}
            message={
              <FormattedMessage
                id="connection.geographyDescription"
                values={{
                  lnk: (node: React.ReactNode) => (
                    <a href={links.cloudAllowlistIPsLink} target="_blank" rel="noreferrer">
                      {node}
                    </a>
                  ),
                }}
              />
            }
          />
        </div>
        <div className={styles.dropdownWrapper}>
          <div className={styles.spinner}>{connectionUpdating && <Spinner small />}</div>
          <div className={styles.dropdown}>
            <DataGeographyDropdown
              isDisabled={connectionUpdating}
              geographies={geographies}
              value={selectedValue || connection.geography || geographies[0]}
              onChange={handleSubmit}
            />
          </div>
        </div>
      </div>
    </Card>
  );
};
