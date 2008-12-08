/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package org.bungeni.editor.selectors.metadata;

import java.util.HashMap;
import org.bungeni.ooo.OOComponentHelper;

/**
 * Used by the BaseMetadataContainerPanel to indicate section metadata editabilty
 * @author Ashok Hariharan
 */
public class SectionMetadataEditor {
     private static org.apache.log4j.Logger log = org.apache.log4j.Logger.getLogger(SectionMetadataEditor.class.getName());
   
    
     /**
      * if section has editable metadata or not
      */
     public boolean bMetadataEditable = false;
    /**
     * metadata variable to indicate true / false for editable metadata
     */
    public static final String MetaEditableFlag = "__BungeniMetaEditable";
    /**
     * metadata variable pointing to actual editor
     */ 
    public static final String MetaEditor = "__BungeniMetaEditor";
    
    private String editableSectionName = "";
    private String metadataEditorString = "";
    /**
     * Constructor to setup a metadata editor object
     * @param sectionName - current section name
     * @param metadataEditor - metadata editor string (toolbarSubAction.ActionName.SubActionName)
     */
    public SectionMetadataEditor(String sectionName, String metadataEditor) {
        editableSectionName = sectionName;
        metadataEditorString = metadataEditor;
    }
    
    /**
     * public function to set metadata editable flag.
     * @param ooDoc - Openoffice component handle
     * @return - true / false indicating success / failure
     */
    public boolean setMetadataEditableFlag(OOComponentHelper ooDoc){
        boolean bState =false;
        try {
            HashMap<String,String>metaMap = new HashMap<String,String>();
            metaMap.put(MetaEditableFlag, "true");
            metaMap.put(MetaEditor, metadataEditorString);
            ooDoc.setSectionMetadataAttributes(editableSectionName, metaMap);
            bState = true;
        } catch(Exception ex) {
            log.error("setMetadataEditableFlag : " + ex.getMessage());
        } finally {
            return bState;
        }
    }
    
    public boolean hasMetadataEditableFlag(OOComponentHelper ooDoc) {
        HashMap<String,String> metaMap = ooDoc.getSectionMetadataAttributes(editableSectionName);
        if (metaMap.containsKey(MetaEditableFlag)) {
            if (metaMap.containsKey(MetaEditor)) {
                return true;
            }
        }
       return false;
    }
}
