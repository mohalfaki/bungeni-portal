/*
 * QuestionText.java
 *
 * Created on August 12, 2008, 2:06 PM
 */

package org.bungeni.editor.selectors.debaterecord.question;

import java.awt.Component;
import java.awt.Toolkit;
import java.awt.datatransfer.Clipboard;
import java.awt.datatransfer.StringSelection;
import java.awt.datatransfer.Transferable;
import java.util.HashMap;
import org.bungeni.editor.selectors.BaseMetadataPanel;
import org.bungeni.utils.CommonDocumentUtilFunctions;

/**
 *
 * @author  undesa
 */
public class QuestionText extends BaseMetadataPanel {

    /** Creates new form QuestionText */
    public QuestionText() {
        initComponents();
    }

    /** This method is called from within the constructor to
     * initialize the form.
     * WARNING: Do NOT modify this code. The content of this method is
     * always regenerated by the Form Editor.
     */
    @SuppressWarnings("unchecked")
    // <editor-fold defaultstate="collapsed" desc="Generated Code">//GEN-BEGIN:initComponents
    private void initComponents() {

        scrollQuestionText = new javax.swing.JScrollPane();
        txtQuestionText = new javax.swing.JTextPane();
        lblQuestionText = new javax.swing.JLabel();

        scrollQuestionText.setName("scroll_question_text"); // NOI18N

        txtQuestionText.setName("txt_question_text"); // NOI18N
        scrollQuestionText.setViewportView(txtQuestionText);

        lblQuestionText.setText("Question Text");
        lblQuestionText.setName("lbl_question_text"); // NOI18N

        javax.swing.GroupLayout layout = new javax.swing.GroupLayout(this);
        this.setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addComponent(scrollQuestionText, javax.swing.GroupLayout.DEFAULT_SIZE, 279, Short.MAX_VALUE)
            .addComponent(lblQuestionText)
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addComponent(lblQuestionText)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(scrollQuestionText, javax.swing.GroupLayout.DEFAULT_SIZE, 112, Short.MAX_VALUE))
        );
    }// </editor-fold>//GEN-END:initComponents


    // Variables declaration - do not modify//GEN-BEGIN:variables
    private javax.swing.JLabel lblQuestionText;
    private javax.swing.JScrollPane scrollQuestionText;
    private javax.swing.JTextPane txtQuestionText;
    // End of variables declaration//GEN-END:variables
public String getPanelName() {
        return getName();
    }

    public Component getPanelComponent() {
        return this;
    }


    @Override
    public boolean doCancel() {
        return true;
    }

    @Override
    public boolean doReset() {
        return true;
    }

    @Override
    public boolean preFullEdit() {
        return true;
    }

    @Override
    public boolean processFullEdit() {
        return true;
    }

    @Override
    public boolean postFullEdit() {
        return true;
    }

    @Override
    public boolean preFullInsert() {
        return true;
    }

    @Override
    public boolean processFullInsert() {
        return true;
    }

    @Override
    public boolean postFullInsert() {
        return true;
    }

    @Override
    public boolean preSelectEdit() {
        return true;
    }

    @Override
    public boolean processSelectEdit() {
        return true;
    }

    @Override
    public boolean postSelectEdit() {
        return true;
    }

    @Override
    public boolean preSelectInsert() {
        return true;
    }

    @Override
    public boolean processSelectInsert() {
        //copy question text to clipboard
        String strText = this.txtQuestionText.getText();
        CommonDocumentUtilFunctions.writeToClipboard(strText);
        /*Clipboard clipBrd = new Clipboard("Clipboard.QuestionText");
        Transferable copyToClipboard = new StringSelection(strText);
        clipBrd.setContents(copyToClipboard, null);*/
        return true;
    }
    
    

    @Override
    public boolean postSelectInsert() {
       return true;
    }

    @Override
    public boolean validateSelectedEdit() {
        return true;
    }

    @Override
    public boolean validateSelectedInsert() {
        return true;
    }

    @Override
    public boolean validateFullInsert() {
        return true;
    }

    @Override
    public boolean validateFullEdit() {
        return true;
    }
    @Override
    protected void initFieldsSelectedEdit() {
        return;
    }

    @Override
    protected void initFieldsSelectedInsert() {
        return;
    }

    @Override
    protected void initFieldsInsert() {
        return;
    }

    @Override
    protected void initFieldsEdit() {
        this.txtQuestionText.setEnabled(false);
        return;
    }
    
    @Override
    public boolean doUpdateEvent(){
        HashMap<String,String> selectionData = ((Main)getContainerPanel()).selectionData;
        if (selectionData != null) {
            if (selectionData.containsKey("QUESTION_TEXT"))
                this.txtQuestionText.setText(selectionData.get("QUESTION_TEXT"));
        }
        return true;
    }
}
