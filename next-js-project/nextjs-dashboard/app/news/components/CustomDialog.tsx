import { Dialog, DialogBackdrop, DialogPositioner, DialogContent, DialogHeader, DialogFooter,  DialogBody, DialogTitle,  DialogCloseTrigger,} from "@chakra-ui/react";
  import { CloseButton, Button } from "@chakra-ui/react";
  import { CustomDialogProps } from "../types";

  const CustomDialog = ({
    dialog,
    onConfirm,
    onCancel,
    title,
    children,
    confirmLabel = "Confirm",
    cancelLabel = "Cancel",
    danger = false,
  }: CustomDialogProps) => {
    return (
      <Dialog.RootProvider value={dialog}>
        <Dialog.Root open={dialog.open}>
          <DialogBackdrop />
          <DialogPositioner>
            <DialogContent>
              <DialogHeader display="flex" justifyContent="space-between" alignItems="center">
                <DialogTitle>{title}</DialogTitle>
                <DialogCloseTrigger asChild>
                  <CloseButton
                    size="sm"
                    onClick={() => {
                      dialog.setOpen(false);
                      onCancel?.(); // si une logique d'annulation est fournie
                    }}
                  />
                </DialogCloseTrigger>
              </DialogHeader>
  
              <DialogBody>{children}</DialogBody>
  
              <DialogFooter>
                <Button variant="outline" onClick={() => {
                  dialog.setOpen(false);
                  onCancel?.();
                }}>
                  {cancelLabel}
                </Button>
                <Button
                  colorPalette={danger ? "red" : "cyan"}
                  variant="outline"
                  onClick={onConfirm}
                >
                  {confirmLabel}
                </Button>
              </DialogFooter>
            </DialogContent>
          </DialogPositioner>
        </Dialog.Root>
      </Dialog.RootProvider>
    );
  };
  
  export default CustomDialog;
  